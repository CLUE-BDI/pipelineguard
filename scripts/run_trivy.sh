#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
trivy fs --format json -o outputs/trivy-fs.json . || true
trivy config --format json -o outputs/trivy-config.json . || true
