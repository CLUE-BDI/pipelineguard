# PipelineGuard Developer Setup Guide

This guide describes how to configure, set up, and run the **PipelineGuard** security analytics data pipeline locally.

---

## 🛠️ 1. Prerequisites & Environment Setup

Ensure you have the following prerequisites installed on your local system:
- **Python**: Version 3.12 or higher.
- **Docker**: For running scanner workloads or isolated container testing.
- **Astral `uv`**: Modern, fast Python package and dependency manager.

### Initialize Virtual Environment
Navigate to the root directory of the repository and install all dependencies:
```bash
# Sync dependencies from uv.lock and set up the local .venv virtual environment
uv sync
```

---

## 🚀 2. Ingesting Telemetry (Phase 0: Scanners)

PipelineGuard ingests telemetry by running local security tools against target codebases and exporting findings to JSON format. We provide helper scripts under the `scripts/` directory:

```bash
# Execute local scan scripts to generate raw outputs in the outputs/ directory
./scripts/scan_gitleaks.sh
./scripts/scan_trivy.sh
./scripts/scan_checkov.sh
./scripts/scan_semgrep.sh
```

---

## 🔄 3. Transforming Telemetry (Phase 1: Normalization)

Once raw JSON artifacts are gathered in the `outputs/` folder, they must be converted into a standardized JSONL schema.

Run the Phase 1 orchestrator script:
```bash
./scripts/run_phase1.sh
```

Under the hood, this executes the python normalization scripts:
*   `scripts/normalize_gitleaks.py`
*   `scripts/normalize_trivy.py`
*   `scripts/normalize_checkov.py`
*   `scripts/normalize_semgrep.py`

Normalized datasets are saved in the `normalized/` folder.

---

## 🧠 4. Correlation & Validation (Phase 2)

Normalized findings are aggregated into deduplicated security incidents with MITRE mapping and risk-based scoring.

Run the Phase 2 orchestrator script:
```bash
./scripts/run_phase2.sh
```

Under the hood, this executes:
1.  **Correlation Engine (`scripts/correlate_findings.py`)**: Merges finding datasets and produces incident reports in `correlated/`.
2.  **Telemetry Validation (`scripts/validate_findings.py` & `scripts/validate_correlation.py`)**: Evaluates schema compliance.
3.  **Threshold Enforcement (`scripts/enforce_thresholds.py`)**: Enforces pipeline quality gates, failing the execution if critical vulnerabilities exceed acceptable limits.
