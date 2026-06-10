#!/usr/bin/env python3
"""
AWS Developer Certification - Exercise Runner
Run exercises, validate solutions, and track progress.
"""

import sys
import os
import json
import importlib.util
from pathlib import Path
from typing import List, Tuple

COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'bold': '\033[1m',
    'end': '\033[0m',
}

def color(text, color_name):
    return f"{COLORS.get(color_name, '')}{text}{COLORS['end']}"

def discover_exercises() -> List[str]:
    """Discover all exercise directories."""
    base = Path(__file__).parent / 'exercises'
    exercises = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and d.name != '__pycache__' and not d.name.startswith('.'):
            exercises.append(str(d))
    return exercises

def run_test(exercise_path: str) -> Tuple[bool, str]:
    """Run the test file for an exercise."""
    exercise_dir = Path(exercise_path)
    test_file = exercise_dir / 'test.py'
    
    if not test_file.exists():
        return False, f"No test.py found in {exercise_dir.name}"
    
    # Clear cached solution module from previous runs
    for mod_name in list(sys.modules.keys()):
        if mod_name in ('solution', 'test'):
            del sys.modules[mod_name]
    
    # Add exercise directory to path
    sys.path.insert(0, str(exercise_dir))
    
    try:
        spec = importlib.util.spec_from_file_location("test", str(test_file))
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Run all test functions
        results = []
        test_functions = [getattr(test_module, name) for name in dir(test_module) 
                         if name.startswith('test_')]
        
        if not test_functions:
            return False, "No test functions found (functions must start with test_)"
        
        passed = 0
        failed = 0
        failures = []
        
        for test_fn in test_functions:
            try:
                test_fn()
                passed += 1
            except AssertionError as e:
                failed += 1
                failures.append(f"  ✗ {test_fn.__name__}: {str(e)}")
            except Exception as e:
                failed += 1
                failures.append(f"  ✗ {test_fn.__name__}: {type(e).__name__}: {str(e)}")
        
        if failed == 0:
            return True, f"All {passed} tests passed! ✓"
        else:
            msg = f"{passed} passed, {failed} failed\n" + "\n".join(failures)
            return False, msg
            
    except Exception as e:
        return False, f"Error loading test: {type(e).__name__}: {str(e)}"
    finally:
        if str(exercise_dir) in sys.path:
            sys.path.remove(str(exercise_dir))

def run_exercise(exercise_path: str) -> bool:
    """Run a single exercise and display results."""
    exercise_dir = Path(exercise_path)
    name = exercise_dir.name
    
    print(color(f"\n{'='*60}", 'blue'))
    print(color(f"  Exercise: {name}", 'bold'))
    print(color(f"{'='*60}", 'blue'))
    
    # Check for README
    readme = exercise_dir / 'README.md'
    if readme.exists():
        print(color(f"  📖 Problem description available", 'yellow'))
    
    # Run test
    success, message = run_test(exercise_path)
    
    if success:
        print(color(f"  ✅ PASSED: {message}", 'green'))
    else:
        print(color(f"  ❌ FAILED: {message}", 'red'))
        print(color(f"  💡 Check the README.md for hints", 'yellow'))
    
    return success

def show_progress():
    """Show overall progress."""
    exercises = discover_exercises()
    
    print(color(f"\n{'='*60}", 'blue'))
    print(color(f"  Progress Report", 'bold'))
    print(color(f"{'='*60}", 'blue'))
    
    passed = 0
    total = len(exercises)
    
    for exercise_path in exercises:
        name = Path(exercise_path).name
        success, _ = run_test(exercise_path)
        status = color("✅ PASS", 'green') if success else color("❌ FAIL", 'red')
        print(f"  {status} - {name}")
        if success:
            passed += 1
    
    print(color(f"\n  {passed}/{total} exercises passed", 'bold'))
    if passed == total:
        print(color("  🎉 Congratulations! All exercises complete!", 'green'))
    print()

def main():
    if len(sys.argv) == 1:
        print(color("\n🏋️ AWS Developer Certification - Exercise Runner\n", 'bold'))
        print("Usage:")
        print("  python runner.py <exercise_path>     Run specific exercise")
        print("  python runner.py --all               Run all exercises")
        print("  python runner.py --progress           Show progress report")
        print("  python runner.py --list               List all exercises")
        return
    
    if '--progress' in sys.argv:
        show_progress()
        return
    
    if '--list' in sys.argv:
        exercises = discover_exercises()
        print(color("\n📚 Available Exercises:\n", 'bold'))
        for ex in exercises:
            print(f"  - {Path(ex).name}")
        print()
        return
    
    if '--all' in sys.argv:
        exercises = discover_exercises()
        results = []
        for ex in exercises:
            results.append(run_exercise(ex))
        
        passed = sum(results)
        total = len(results)
        print(color(f"\n{'='*60}", 'blue'))
        print(color(f"  Results: {passed}/{total} passed", 'bold'))
        print(color(f"{'='*60}", 'blue'))
        return
    
    # Run specific exercises
    results = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            results.append(run_exercise(arg))
        else:
            print(color(f"  ⚠️ Directory not found: {arg}", 'yellow'))

if __name__ == '__main__':
    main()
