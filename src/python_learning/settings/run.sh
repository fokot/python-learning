#!/usr/bin/env bash
# Demo runner: sets env vars, then runs settings.py.
set -euo pipefail

# 2. Env vars — names are APP_<FIELD> because of env_prefix="APP_".
#    APP_NAME also overrides the default in code.
export APP_NAME="my-app"
export APP_LOG_LEVEL="DEBUG"
# export APP_PORT="9000"                              # string in env, becomes int
export APP_ALLOWED_HOSTS='["localhost","127.0.0.1"]'  # JSON for list fields

# 3. Run it.
cd "$(dirname "$0")/../../.."
uv run python -m python_learning.settings.settings
