# 🚀 PipelineGuard — Multi-Cloud Security Data Engineering Platform

## 📌 Overview

**PipelineGuard** is a **data engineering platform for security analytics**, designed to ingest, transform, and analyze vulnerability data generated across modern CI/CD pipelines.

The system transforms raw security scan outputs into a **structured, analytics-ready dataset**, enabling:

* Cross-tool vulnerability correlation
* MITRE ATT&CK mapping
* Risk-based prioritization
* Scalable analytics and reporting

---

## 🏗️ Architecture

PipelineGuard follows a **modern data engineering architecture**:

```text
Sources → Ingestion → Processing → Storage → Analytics → Visualization
```

### Core Principles

* Batch-first ingestion
* Schema standardization (JSONL)
* Layered data processing
* Separation of compute and storage
* Multi-cloud execution with centralized analytics

---

## 🧱 Data Pipeline

### 🔴 1. Data Sources

Security tools generate raw findings:

* Gitleaks (secrets detection)
* Trivy (container & dependency vulnerabilities)
* Checkov (IaC misconfigurations)
* Semgrep (code-level issues)

Output format:

```json
Raw JSON scan results
```

---

### 🟠 2. Ingestion Layer

PipelineGuard orchestrates ingestion via:

* Docker containers (local development)
* AWS ECS (batch execution)
* Azure AKS (workers & services)
* CI/CD pipelines (GitLab)

Output:

```text
Raw findings stored as JSON artifacts
```

---

### 🔵 3. Processing Layer

The core data engineering pipeline consists of:

#### ✅ Normalization

* Converts tool-specific outputs into a unified schema
* Produces JSONL records
* Standardizes severity and metadata

#### ✅ Enrichment

* Maps findings to MITRE ATT&CK
* Adds contextual metadata
* Enhances classification

#### ✅ Correlation

* Groups findings into incidents
* Deduplicates signals across tools
* Applies risk scoring

Output:

```text
Normalized + Correlated JSONL datasets
```

---

### 🟢 4. Storage Layer

#### Data Lake (GCS)

* Stores raw and processed artifacts
* Structure:

```text
gs://pipelineguard-artifacts/
  ├── raw/
  ├── normalized/
  └── correlated/
```

#### Data Warehouse (BigQuery)

Dataset:

```text
pipelineguard_analytics
```

Tables:

* `findings_normalized`
* `incidents`
* `correlated_findings`

Data is loaded from GCS using batch load jobs.

---

### 🟣 5. Analytics Layer

#### SQL Modeling

* 24 analytical views
* MITRE mapping
* Severity trends
* Risk scoring
* Incident aggregation

#### Visualization

* Looker Studio dashboards
* Real-time exploration of security posture

---

## ☁️ Multi-Cloud Execution

### AWS (ECS Fargate)

* Batch processing layer
* Scheduled ingestion jobs
* Blue/Green deployments

### Azure (AKS)

* API and worker services
* Distributed processing
* Blue/Green cluster strategy

### GCP

* Data lake (GCS)
* Data warehouse (BigQuery)
* Analytics (Looker Studio)

---

## 🐳 Containerized Architecture

| Component                | Description                       |
| ------------------------ | --------------------------------- |
| `pipelineguard-scanners` | Data ingestion (scan execution)   |
| `pipelineguard-runtime`  | Data transformation + correlation |
| `gcp-jobs`               | Data loading & SQL execution      |

---

## ⚙️ CI/CD Pipeline

Pipeline stages:

```text
Build → Ingest → Normalize → Correlate → Validate → Load → Transform → Deploy
```

CI/CD handles:

* Container builds
* Data pipeline execution
* BigQuery loading
* View generation
* Multi-cloud deployment

---

## 🗂️ Project Structure

```text
pipelineguard/
│
├── scripts/
│   ├── run_phase1.sh
│   ├── run_phase2.sh
│   ├── normalize_*.py
│   ├── correlate_findings.py
│   └── validate_*.py
│
├── sql/
│   └── views/
│
├── outputs/
├── normalized/
├── correlated/
│
├── Dockerfile.runtime
├── Dockerfile.scanners
├── .gitlab-ci.yml
│
└── terraform/
```

---

## 🛠️ Local Development

### Build images

```bash
docker build -f Dockerfile.scanners -t pipelineguard-scanners .
docker build -f Dockerfile.runtime -t pipelineguard-runtime .
```

### Run ingestion

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  -e TARGET_REPO_NAME=terragoat \
  pipelineguard-scanners \
  bash -lc './scripts/run_phase1.sh'
```

### Run processing

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  pipelineguard-runtime \
  bash -lc './scripts/run_phase2.sh && uv run python -m scripts.correlate_findings'
```

---

## 📊 Data Flow Summary

```text
Security Tools → JSON → Normalize → Enrich → Correlate
              → GCS → BigQuery → Views → Dashboard
```

---

## 🔐 Security

* AWS Secrets Manager
* Azure Key Vault
* GCP Service Accounts

Credentials are injected at runtime.

---

## 📈 Future Enhancements

* Streaming ingestion (Kafka / Kinesis)
* ML-based anomaly detection
* Automated remediation workflows
* Data quality validation layer
* Real-time dashboards

---

## 🎯 Key Data Engineering Concepts

* Batch data pipelines
* Schema normalization
* Data lake + warehouse architecture
* Multi-cloud compute
* Analytical modeling (SQL views)
* Observability & validation

---

## 👤 Author

**Md Hasan**
Cloud Platform Security | Data Engineering | DevSecOps

---

## ⭐ Summary

PipelineGuard demonstrates how **security telemetry can be transformed into a scalable data platform**, enabling:

* Unified visibility across tools
* Data-driven risk prioritization
* Enterprise-grade analytics

---
