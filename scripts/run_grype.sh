#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
docker build -t pipelineguard-lab:latest -f docker/Dockerfile . || true
grype pipelineguard-lab:latest -o json > outputs/grype.json || true
