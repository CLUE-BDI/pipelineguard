#!/usr/bin/env bash
set -euo pipefail
# source config/target.env

mkdir -p "outputs/${TARGET_REPO_NAME}"
uv run checkov -d "${TARGET_REPO_PATH}" -o json > "outputs/${TARGET_REPO_NAME}/checkov.json" || true
