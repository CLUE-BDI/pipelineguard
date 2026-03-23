#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
checkov -d . -o json > outputs/checkov.json || true
