# PipelineGuard Deployment & Cloud Setup Guide

This guide details the steps to deploy the **PipelineGuard** telemetry collection pipeline to Google Cloud Platform (GCP) and integrate it with your CI/CD runner.

---

## ── SECTION 1: GOOGLE CLOUD PLATFORM CONFIGURATION ───────────────────────────

PipelineGuard uses **Google Cloud Storage (GCS)** as a landing data lake and **Google BigQuery** as the analytical data warehouse.

### 🪣 1.1 GCS Data Lake Setup
Create a GCS bucket to store telemetry history. Organize it with the following partition namespaces:
```text
gs://<your-bucket-name>/
  ├── raw/          # Raw scanner JSON logs
  ├── normalized/   # Unified JSONL findings
  └── correlated/   # Aggregated incidents
```

Create the bucket using the Google Cloud SDK `gcloud` or `gsutil`:
```bash
gsutil mb -l us-central1 gs://pipelineguard-artifacts-prod
```

### 📊 1.2 BigQuery Data Warehouse Setup
Create a dataset named `pipelineguard_analytics` and define your schemas for loading the structured `jsonl` files from GCS:

1.  **Create the Dataset**:
    ```bash
    bq mk --location=US pipelineguard_analytics
    ```
2.  **Tables Schema Mappings**:
    Define schemas matching the Pydantic schemas in `scripts/common.py` for:
    *   `findings_normalized`
    *   `incidents`
    *   `correlated_findings`

---

## ── SECTION 2: ACCESS CONTROL & CREDENTIALS ──────────────────────────────────

To enable the automated pipelines to push findings, you must provision a GCP Service Account.

1.  **Create the Service Account**:
    ```bash
    gcloud iam service-accounts create pipelineguard-writer \
      --description="Service account for PipelineGuard CI/CD data ingestion" \
      --display-name="pipelineguard-writer"
    ```
2.  **Assign Required Roles**:
    *   **Storage Object Admin** (`roles/storage.objectAdmin`): To upload findings to GCS.
    *   **BigQuery Data Editor** (`roles/bigquery.dataEditor`): To insert entries into BigQuery tables.
    *   **BigQuery Job User** (`roles/bigquery.jobUser`): To execute load jobs in BigQuery.
3.  **Generate Private JSON Key**:
    ```bash
    gcloud iam service-accounts keys create ~/keys/pipelineguard-key.json \
      --iam-account=pipelineguard-writer@<YOUR-PROJECT-ID>.iam.gserviceaccount.com
    ```
4.  **Local Authentication Variable**:
    Set the environment variable pointing to the credentials key:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/home/demo/keys/pipelineguard-key.json"
    ```

---

## ── SECTION 3: CI/CD PIPELINE INTEGRATION ────────────────────────────────────

PipelineGuard pipelines are automated via **GitLab CI/CD** (configured in `.gitlab-ci.yml`).

### CI Execution Flow
Every commit or scheduled scan executes the following stages:
1.  **Scanner Jobs**: Runs Gitleaks, Trivy, Checkov, and Semgrep container jobs on the target repositories.
2.  **Process Job**: Spawns the `pipelineguard-runtime` container to run `normalize` and `correlate` stages.
3.  **Cloud Load Job**: Authenticates via the masked `GCP_SERVICE_KEY` environment variable, uploads the result datasets to GCS, and triggers the `bq load` command to push them to BigQuery.
