# Setup

Get your machine ready for the DVA-C02 study path (offline exercises + LocalStack labs).

## Prerequisites

- **Python 3.11+** (`python --version`)
- **Docker Desktop** (or Docker Engine + Compose v2)
- Git (to clone this repo)

## Install Python deps

From the repo root:

```bash
python -m venv .venv

# Windows (Git Bash / PowerShell)
source .venv/Scripts/activate   # or: .venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Start LocalStack

```bash
docker compose up -d
```

Wait until LocalStack is healthy, then check:

```bash
curl http://localhost:4566/_localstack/health
# or
awslocal s3 ls
```

Stop with `docker compose down`.

## Environment variables

Point the AWS SDK and CLI at LocalStack (dummy credentials are fine):

```bash
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
```

On Windows PowerShell:

```powershell
$env:AWS_ENDPOINT_URL="http://localhost:4566"
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"
```

Lab exercises also use `common/aws_client.py`, which reads these defaults automatically.

## Cursor Agent + Git (optional)

Agent git commits use the global Cursor rule `~/.cursor/rules/git-commits.mdc` (HEREDOC + `Co-authored-by: Cursor <cursoragent@cursor.com>`). For optional GitHub MCP / `gh` / Cloud Agents, see `~/.cursor/github-mcp-setup.md`. Unrelated to LocalStack.

## Verify the runner (no LocalStack needed)

```bash
python runner.py --list
python runner.py exercises/01-lambda-basics --solution
```

Default runs test your `starter.py`. Use `--solution` to validate the answer key.
