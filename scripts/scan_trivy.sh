#!/usr/bin/env bash
set -euo pipefail
# source config/target.env

: "${TARGET_REPO_NAME:?TARGET_REPO_NAME is not set}"
: "${TARGET_REPO_PATH:?TARGET_REPO_PATH is not set}"

mkdir -p "outputs/${TARGET_REPO_NAME}"
IGNORE_FLAG=""
if [ -f "${TARGET_REPO_PATH}/.trivyignore" ]; then
  IGNORE_FLAG="--ignorefile ${TARGET_REPO_PATH}/.trivyignore"
fi

trivy fs $IGNORE_FLAG --cache-dir .trivycache --format json -o "outputs/${TARGET_REPO_NAME}/trivy-fs.json" "${TARGET_REPO_PATH}" || true
trivy config $IGNORE_FLAG --cache-dir .trivycache --format json -o "outputs/${TARGET_REPO_NAME}/trivy-config.json" "${TARGET_REPO_PATH}" || true