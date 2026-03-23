#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
kube-score score k8s/deployment.yaml > outputs/kube-score.txt || true
