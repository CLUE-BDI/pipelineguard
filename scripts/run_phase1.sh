#!/usr/bin/env bash
set -euo pipefail

: "${TARGET_REPO_NAME:?TARGET_REPO_NAME is not set}"
: "${TARGET_REPO_PATH:?TARGET_REPO_PATH is not set}"

if [[ ! -d "${TARGET_REPO_PATH}" ]]; then
  echo "ERROR: Target repo does not exist: ${TARGET_REPO_PATH}"
  exit 1
fi

./scripts/scan_gitleaks.sh
./scripts/scan_trivy.sh
./scripts/scan_checkov.sh
./scripts/scan_semgrep.sh

echo
echo "Phase 1 outputs written to outputs/${TARGET_REPO_NAME}/"
ls -lh "outputs/${TARGET_REPO_NAME}/"