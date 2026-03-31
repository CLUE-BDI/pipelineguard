#!/usr/bin/env bash
set -euo pipefail

echo "Repo: ${TARGET_REPO_NAME}"
find "outputs/${TARGET_REPO_NAME}" -maxdepth 1 -type f | sort || true

uv run python -m scripts.normalize_gitleaks
uv run python -m scripts.normalize_checkov
uv run python -m scripts.normalize_semgrep
uv run python -m scripts.normalize_trivy

echo "Normalized files:"
find "normalized/${TARGET_REPO_NAME}" -maxdepth 1 -type f | sort || true

uv run python -m scripts.merge_findings
uv run python -m scripts.validate_findings

echo
echo "Phase 2 complete for ${TARGET_REPO_NAME}"