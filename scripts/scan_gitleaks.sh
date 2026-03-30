#!/usr/bin/env bash
set -euo pipefail
# source config/target.env

: "${TARGET_REPO_NAME:?TARGET_REPO_NAME is not set}"
: "${TARGET_REPO_PATH:?TARGET_REPO_PATH is not set}"

mkdir -p "outputs/${TARGET_REPO_NAME}"
gitleaks detect --source "${TARGET_REPO_PATH}" --report-format json --report-path "outputs/${TARGET_REPO_NAME}/gitleaks.json" || true