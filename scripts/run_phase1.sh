#!/usr/bin/env bash
set -euo pipefail
source config/target.env

./scripts/scan_gitleaks.sh
./scripts/scan_trivy.sh
./scripts/scan_checkov.sh
./scripts/scan_semgrep.sh

echo
echo "Phase 1 outputs written to outputs/${TARGET_REPO_NAME}/"
ls -lh "outputs/${TARGET_REPO_NAME}/"