#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
semgrep --config auto --json --output outputs/semgrep.json . || true
