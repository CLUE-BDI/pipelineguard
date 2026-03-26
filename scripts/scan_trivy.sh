#!/usr/bin/env bash
set -euo pipefail
source config/target.env

mkdir -p "outputs/${TARGET_REPO_NAME}"
trivy fs --format json -o "outputs/${TARGET_REPO_NAME}/trivy-fs.json" "${TARGET_REPO_PATH}" || true
trivy config --format json -o "outputs/${TARGET_REPO_NAME}/trivy-config.json" "${TARGET_REPO_PATH}" || true