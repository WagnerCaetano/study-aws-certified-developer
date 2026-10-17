#!/usr/bin/env python3
"""
AWS Developer Certification - Exercise Runner

By default tests starter.py. Use --solution to validate solution.py.
Progress for starter passes is stored in .progress.json.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent
PROGRESS_FILE = ROOT / ".progress.json"

COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "bold": "\033[1m",
    "end": "\033[0m",
}

# Exercise number ranges by exam domain (folders under exercises/)
DOMAIN_RANGES = {
    "development": range(1, 15),   # 01-14
    "security": range(15, 21),     # 15-20
    "deployment": range(21, 27),   # 21-26 (+ 35 handled below)
    "monitoring": range(27, 31),   # 27-30
}

DEPLOYMENT_EXTRA = {35}  # advanced CI/CD scenario
ADVANCED_SCENARIOS = range(31, 35)  # 31-34: multi-service concept checks


def color(text: str, color_name: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"{COLORS.get(color_name, '')}{text}{COLORS['end']}"


def load_progress() -> Dict[str, bool]:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_progress(progress: Dict[str, bool]) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def exercise_number(name: str) -> Optional[int]:
    prefix = name.split("-", 1)[0]
    if prefix.isdigit():
        return int(prefix)
    return None


def discover_under(base: Path) -> List[Path]:
    if not base.is_dir():
        return []
    found: List[Path] = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name != "__pycache__":
            if (d / "test.py").exists():
                found.append(d)
    return found


def discover_exercises() -> List[Path]:
    return discover_under(ROOT / "exercises") + discover_under(ROOT / "labs")


def filter_by_domain(exercises: List[Path], domain: str) -> List[Path]:
    domain = domain.lower()
    if domain not in DOMAIN_RANGES and domain != "monitoring":
        raise SystemExit(
            f"Unknown domain '{domain}'. "
            "Use: development, security, deployment, monitoring"
        )

    allowed = set(DOMAIN_RANGES[domain])
    if domain == "deployment":
        allowed |= DEPLOYMENT_EXTRA
    if domain == "development":
        # advanced 31-34 stay listed under development catalog but
        # are not in range 1-14; include them when filtering development
        # only via --all / explicit path. Domain filter = core domain ranges.
        pass

    result = []
    for path in exercises:
        num = exercise_number(path.name)
        if num is not None and num in allowed:
            result.append(path)
    return result


def resolve_path(arg: str) -> Path:
    p = Path(arg)
    if not p.is_absolute():
        p = (ROOT / p).resolve()
    else:
        p = p.resolve()
    return p


def clear_exercise_modules() -> None:
    for mod_name in list(sys.modules.keys()):
        if mod_name in ("starter", "solution", "test") or mod_name.startswith(
            ("starter.", "solution.", "test.")
        ):
            del sys.modules[mod_name]


def is_localstack_exercise(exercise_dir: Path) -> bool:
    """True when the exercise ships a ``.localstack`` marker file."""
    return (exercise_dir / ".localstack").is_file()


def warn_if_localstack_down(exercise_dir: Path) -> None:
    if not is_localstack_exercise(exercise_dir):
        return
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        from common.aws_client import is_localstack_up
    except ImportError:
        print(
            color(
                "  ⚠️  LocalStack exercise, but common.aws_client could not be imported",
                "yellow",
            )
        )
        return
    if not is_localstack_up():
        print(
            color(
                "  ⚠️  LocalStack appears down — start with: docker compose up -d",
                "yellow",
            )
        )


def run_test(exercise_dir: Path, module_under_test: str) -> Tuple[bool, str]:
    """Run test.py with EXERCISE_MODULE set to starter or solution."""
    test_file = exercise_dir / "test.py"
    if not test_file.exists():
        return False, f"No test.py found in {exercise_dir.name}"

    target = exercise_dir / f"{module_under_test}.py"
    if not target.exists():
        return False, f"Missing {module_under_test}.py in {exercise_dir.name}"

    clear_exercise_modules()
    os.environ["EXERCISE_MODULE"] = module_under_test

    # Repo root first so labs/exercises can `import common`
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(exercise_dir))
    try:
        spec = importlib.util.spec_from_file_location(
            f"exercise_test_{exercise_dir.name}",
            str(test_file),
        )
        if spec is None or spec.loader is None:
            return False, "Could not load test module"
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        test_functions = [
            getattr(test_module, name)
            for name in dir(test_module)
            if name.startswith("test_") and callable(getattr(test_module, name))
        ]
        if not test_functions:
            return False, "No test functions found (names must start with test_)"

        passed = 0
        failures: List[str] = []
        for test_fn in test_functions:
            try:
                test_fn()
                passed += 1
            except AssertionError as e:
                failures.append(f"  ✗ {test_fn.__name__}: {e}")
            except Exception as e:
                failures.append(
                    f"  ✗ {test_fn.__name__}: {type(e).__name__}: {e}"
                )

        if not failures:
            return True, f"All {passed} tests passed! ✓"
        failed = len(failures)
        return False, f"{passed} passed, {failed} failed\n" + "\n".join(failures)
    except Exception as e:
        return False, f"Error loading test: {type(e).__name__}: {e}"
    finally:
        if str(exercise_dir) in sys.path:
            sys.path.remove(str(exercise_dir))
        clear_exercise_modules()


def run_exercise(
    exercise_dir: Path,
    *,
    use_solution: bool = False,
    update_progress: bool = True,
) -> bool:
    name = exercise_dir.name
    module = "solution" if use_solution else "starter"
    label = "solution" if use_solution else "starter"

    print(color(f"\n{'=' * 60}", "blue"))
    print(color(f"  Exercise: {name}  [{label}]", "bold"))
    print(color(f"{'=' * 60}", "blue"))

    if (exercise_dir / "README.md").exists():
        print(color("  📖 Problem description available", "yellow"))

    if is_localstack_exercise(exercise_dir):
        print(color("  🐳 LocalStack-backed exercise", "blue"))
        warn_if_localstack_down(exercise_dir)

    success, message = run_test(exercise_dir, module)

    if success:
        print(color(f"  ✅ PASSED: {message}", "green"))
        if update_progress and not use_solution:
            progress = load_progress()
            progress[name] = True
            save_progress(progress)
    else:
        print(color(f"  ❌ FAILED: {message}", "red"))
        print(color("  💡 Check README.md for hints", "yellow"))
        if update_progress and not use_solution:
            progress = load_progress()
            progress[name] = False
            save_progress(progress)

    return success


def show_list(exercises: List[Path]) -> None:
    print(color("\n📚 Available Exercises:\n", "bold"))
    progress = load_progress()
    for ex in exercises:
        done = progress.get(ex.name)
        mark = ""
        if done is True:
            mark = color(" ✓", "green")
        elif done is False:
            mark = color(" ·", "yellow")
        ls = color(" [LS]", "blue") if is_localstack_exercise(ex) else ""
        print(f"  - {ex.relative_to(ROOT)}{ls}{mark}")
    print()


def show_progress(exercises: List[Path]) -> None:
    progress = load_progress()
    print(color(f"\n{'=' * 60}", "blue"))
    print(color("  Progress Report (starter.py)", "bold"))
    print(color(f"{'=' * 60}", "blue"))

    passed = 0
    for ex in exercises:
        status = progress.get(ex.name)
        if status is True:
            print(f"  {color('✅ PASS', 'green')} - {ex.name}")
            passed += 1
        elif status is False:
            print(f"  {color('❌ FAIL', 'red')} - {ex.name}")
        else:
            print(f"  {color('⬜ TODO', 'yellow')} - {ex.name}")

    total = len(exercises)
    print(color(f"\n  {passed}/{total} starters passed (from .progress.json)", "bold"))
    if passed == total and total > 0:
        print(color("  🎉 Congratulations! All exercises complete!", "green"))
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run DVA-C02 exercise tests (starter by default).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Exercise or lab path(s), e.g. exercises/01-lambda-basics",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all discovered exercises and labs",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all exercises",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show starter progress from .progress.json",
    )
    parser.add_argument(
        "--domain",
        choices=["development", "security", "deployment", "monitoring"],
        help="Filter exercises by exam domain",
    )
    parser.add_argument(
        "--solution",
        action="store_true",
        help="Test solution.py instead of starter.py",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    all_exercises = discover_exercises()

    if args.list:
        targets = (
            filter_by_domain(all_exercises, args.domain)
            if args.domain
            else all_exercises
        )
        show_list(targets)
        return 0

    if args.progress:
        targets = (
            filter_by_domain(all_exercises, args.domain)
            if args.domain
            else all_exercises
        )
        show_progress(targets)
        return 0

    if args.all or args.domain:
        targets = all_exercises
        if args.domain:
            targets = filter_by_domain(targets, args.domain)
        if not targets:
            print(color("No exercises found for that filter.", "yellow"))
            return 1
        results = [
            run_exercise(ex, use_solution=args.solution, update_progress=not args.solution)
            for ex in targets
        ]
        passed = sum(results)
        total = len(results)
        print(color(f"\n{'=' * 60}", "blue"))
        print(color(f"  Results: {passed}/{total} passed", "bold"))
        print(color(f"{'=' * 60}", "blue"))
        return 0 if passed == total else 1

    if not args.paths:
        parser.print_help()
        return 0

    results = []
    for arg in args.paths:
        path = resolve_path(arg)
        if not path.is_dir():
            print(color(f"  ⚠️ Directory not found: {arg}", "yellow"))
            results.append(False)
            continue
        results.append(
            run_exercise(
                path,
                use_solution=args.solution,
                update_progress=not args.solution,
            )
        )

    if len(results) > 1:
        passed = sum(results)
        print(color(f"\n  Results: {passed}/{len(results)} passed", "bold"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
