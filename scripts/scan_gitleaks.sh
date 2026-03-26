#!/usr/bin/env bash
set -euo pipefail
source config/target.env

mkdir -p "outputs/${TARGET_REPO_NAME}"
gitleaks detect --source "${TARGET_REPO_PATH}" --report-format json --report-path "outputs/${TARGET_REPO_NAME}/gitleaks.json" || true