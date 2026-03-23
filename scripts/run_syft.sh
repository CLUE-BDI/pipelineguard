#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
syft dir:. -o json > outputs/syft.json || true
