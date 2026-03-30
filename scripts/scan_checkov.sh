#!/usr/bin/env bash
set -euo pipefail
# source config/target.env

: "${TARGET_REPO_NAME:?TARGET_REPO_NAME is not set}"
: "${TARGET_REPO_PATH:?TARGET_REPO_PATH is not set}"

mkdir -p "outputs/${TARGET_REPO_NAME}"
uv run checkov -d "${TARGET_REPO_PATH}" -o json > "outputs/${TARGET_REPO_NAME}/checkov.json" || true
