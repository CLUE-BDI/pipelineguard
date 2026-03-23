#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
gitleaks detect --source . --report-format json --report-path outputs/gitleaks.json || true
