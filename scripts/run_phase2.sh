#!/usr/bin/env bash
set -euo pipefail

uv run python -m scripts.normalize_gitleaks
uv run python -m scripts.normalize_checkov
uv run python -m scripts.normalize_semgrep
uv run python -m scripts.normalize_trivy
uv run python -m scripts.merge_findings
uv run python -m scripts.validate_findings

echo
echo "Phase 2 complete for ${TARGET_REPO_NAME}"
