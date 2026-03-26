#!/usr/bin/env bash
set -euo pipefail
source config/target.env

mkdir -p "outputs/${TARGET_REPO_NAME}"
uv run semgrep --config auto --json --no-git-ignore --output "outputs/${TARGET_REPO_NAME}/semgrep.json" "${TARGET_REPO_PATH}" || true