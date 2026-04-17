# 🚀 PipelineGuard — Multi-Cloud Security Data Engineering Platform

## 📊 Live Dashboard

👉 https://datastudio.google.com/u/1/reporting/fb711dfb-2354-42b9-9d7e-62464853ce48/page/F4TtF

<p align="center">
  <img src="./docs/images/pipelineguard-dezoomcamp.drawio.png" width="100%">
</p>

<p align="center">
  <em>Figure: PipelineGuard Multi-Cloud Data Engineering Architecture</em>
</p>

---

## 📌 Overview

**PipelineGuard** is a **data engineering platform for security analytics** that ingests, transforms, and analyzes vulnerability data across modern CI/CD pipelines.

It converts raw security scan outputs into **structured, analytics-ready datasets**, enabling:

- Cross-tool vulnerability correlation  
- MITRE ATT&CK mapping  
- Risk-based prioritization  
- Scalable analytics and reporting  

---

## 📊 Live Dashboard (Visualization)

<p align="center">
  <a href="https://datastudio.google.com/u/1/reporting/fb711dfb-2354-42b9-9d7e-62464853ce48/page/F4TtF" target="_blank">
    <img src="https://img.shields.io/badge/View-Dashboard-blue?style=for-the-badge&logo=googleanalytics" />
  </a>
</p>

PipelineGuard includes a live analytics dashboard built using **Looker Studio (Google Data Studio)**.

👉 **Access the dashboard:**
https://datastudio.google.com/u/1/reporting/fb711dfb-2354-42b9-9d7e-62464853ce48/page/F4TtF

---

### 📈 Dashboard Highlights

The dashboard provides insights across the full data pipeline:

#### 🧭 Executive Overview

* Total findings
* Critical & high severity issues
* Secret exposure count
* Top repositories by risk

#### 📊 Findings Analysis

* Findings by severity
* Findings by tool (Gitleaks, Trivy, Checkov, Semgrep)
* Findings by category (IaC, K8s, secrets, code)

#### ⚠️ Incident Analysis

* Correlated incidents
* Risk scoring per repository
* Incident trends over time

#### 🧠 MITRE ATT&CK Coverage

* Findings mapped to MITRE techniques
* Coverage distribution across attack categories

---

### 🔄 Data Pipeline Behind the Dashboard

```text
Security Tools → Normalize → Correlate → GCS → BigQuery → SQL Views → Looker Studio
```

---

### 🧠 Purpose

This dashboard demonstrates:

* End-to-end data pipeline execution
* Analytical modeling using BigQuery
* Real-time visualization of security data
* Data-driven risk prioritization

---


## 🧪 Vulnerable Data Sources (Test Repositories)

PipelineGuard ingests data from intentionally vulnerable open-source repositories to simulate real-world security scenarios across multiple domains.

These repositories act as **data sources** for the pipeline and enable end-to-end testing of ingestion, normalization, correlation, and analytics.

These repositories simulate heterogeneous upstream data sources in a production data pipeline.

---

### 🔴 Infrastructure as Code (IaC)

* 🔗 https://github.com/bridgecrewio/terragoat

  * Terraform misconfigurations
  * Used to test **Checkov** and IaC scanning

---

### ☸️ Kubernetes Security

* 🔗 https://github.com/madhuakula/kubernetes-goat

  * Vulnerable Kubernetes manifests
  * Used to test **k8s misconfiguration detection**

---

### 🧾 Application Security

* 🔗 https://github.com/juice-shop/juice-shop

  * OWASP Juice Shop (intentionally vulnerable web app)
  * Used to test **Semgrep and code analysis**

---

### 🔐 Secrets Detection

* 🔗 https://github.com/gitleaks/gitleaks/tree/master/testdata

  * Embedded secrets across multiple formats
  * Used to test **Gitleaks secret detection**

---

### 🧪 Custom Multi-Layer Test Dataset

* 📁 `vulnerable-repos/secrets-lab/`

  * Combined dataset including:

    * `.env` files (credentials)
    * Terraform configs
    * Kubernetes YAML
    * Application code
  * Designed to simulate **real enterprise data pipelines**

---

## 📊 How These Fit Into the Data Pipeline

```text
Vulnerable Repos → Scan Tools → JSON Output
                 → Normalize → Correlate → Store → Analyze
```

Each repository contributes different **signal types**:

| Repo               | Signal Type   | Tool            |
| ------------------ | ------------- | --------------- |
| Terragoat          | IaC Misconfig | Checkov         |
| Kubernetes Goat    | K8s Misconfig | Checkov / Trivy |
| Juice Shop         | Code Issues   | Semgrep         |
| Gitleaks Test Data | Secrets       | Gitleaks        |
| Secrets Lab        | Mixed         | All Tools       |

---

## 🎯 Purpose

These datasets enable:

* Multi-source data ingestion
* Cross-domain correlation
* Realistic security analytics
* Validation of data engineering pipelines

---


## 🏗️ Architecture

PipelineGuard follows a **modern batch-oriented data pipeline architecture**:


```text
Sources → Ingestion → Processing → Storage → Analytics → Visualization
```
---

## 🔎 Architecture Overview

### 🔴 Data Sources
Security tools generate raw findings:
- Gitleaks (secrets detection)  
- Trivy (container & dependency vulnerabilities)  
- Checkov (IaC misconfigurations)  
- Semgrep (code-level issues)  

Output:

```json
Raw JSON scan results
```

---

### 🟠 Ingestion Layer

- Docker-based execution (local development)  
- AWS ECS (batch jobs)  
- Azure AKS (distributed workers)  
- GitLab CI/CD orchestration  

Output:

```json
Raw scan artifacts (JSON)
```
---

### 🔵 Processing Layer (Core Data Engineering)

#### ✅ Normalization
- Converts tool-specific outputs into a unified schema  
- Transforms JSON → JSONL  
- Standardizes severity and metadata  

#### ✅ Enrichment
- MITRE ATT&CK mapping  
- Metadata augmentation  
- Severity normalization  

#### ✅ Correlation
- Groups findings into incidents  
- Deduplicates overlapping signals  
- Applies risk scoring  

Output:

```json
Normalized + Correlated JSONL datasets
```

---

### 🟢 Storage Layer

#### Data Lake — GCS

* Stores raw and processed artifacts
* Structure:

```json
gs://pipelineguard-artifacts/
  ├── raw/
  ├── normalized/
  └── correlated/
```

#### Data Warehouse (BigQuery)

Dataset:

```json
pipelineguard_analytics
```

Tables:

* `findings_normalized`
* `incidents`
* `correlated_findings`

Data is loaded from GCS using batch load jobs.

---

### 🟣 Analytics Layer

#### SQL Transformation Layer
- 24 analytical views  
- Severity distribution  
- MITRE mapping  
- Risk scoring  
- Incident aggregation  

#### Visualization
- Looker Studio dashboards  
- Real-time exploration of security posture  

---

## ☁️ Multi-Cloud Architecture

| Cloud | Role |
|------|------|
| **AWS ECS (Fargate)** | Batch compute for scanning & processing | [Future Enhancements] |
| **Azure AKS** | API layer + distributed workers | [Future Enhancements] |
| **GCP** | Data lake (GCS) + Data warehouse (BigQuery) + Analytics | [MVP] |

## 🐳 Containerized Components

| Component | Description |
|----------|------------|
| `pipelineguard-scanners` | Executes security scans (ingestion) |
| `pipelineguard-runtime` | Normalization + correlation engine |
| `gcp-jobs` | BigQuery + GCS operations |

---

## ⚙️ CI/CD Pipeline

Implemented using **GitLab CI/CD**

### Stages

```text
Build → Ingest → Normalize → Correlate → Validate → Load → Transform → Deploy
```

Responsibilities:
- Build and push containers  
- Execute data pipelines  
- Upload artifacts to GCS  
- Load data into BigQuery  
- Apply SQL views  
- Deploy to AWS & Azure  

---

## 🗂️ Project Structure

```text
pipelineguard/
│
.
.
.
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
├── docs/
│ ├── images/
│ │ └── pipelineguard-architecture.png
│ └── diagrams/
│ └── pipelineguard-architecture.drawio
.
.
.
```

## 📊 Data Flow Summary

```text
Security Tools → JSON → Normalize → Enrich → Correlate
              → GCS → BigQuery → Views → Dashboard
```

---

## 🔧 Architecture Diagram Source

👉 [Edit in draw.io](https://app.diagrams.net/?url=https://gitlab.com/datatalks.club/pipelineguard/-/raw/pipelineguard-arch-mvp/docs/diagrams/pipelineguard-dezoomcamp.drawio)

---

## 🔐 Security & Secrets

* AWS Secrets Manager
* Azure Key Vault
* GCP Service Accounts

Environment variable:

GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

---

## 📈 Future Enhancements

* Streaming ingestion (Kafka / Kinesis)
* ML-based anomaly detection
* Automated remediation workflows
* SBOM integration (Syft / Grype)
* Policy-as-code (OPA / Rego)
* Multi-cloud compute separation

## 🎯 Key Data Engineering Concepts

* Batch data pipelines
* Schema normalization (JSON → JSONL)
* Data lake + warehouse architecture
* SQL-based analytical modeling
* Data validation and observability

---

## 👤 Author

**Md Hasan**
Cloud Platform Security | Data Engineering | DevSecOps

---

⭐ Summary

PipelineGuard demonstrates how security telemetry can be transformed into a scalable data engineering platform, enabling:

Unified visibility across tools
Data-driven risk prioritization
Enterprise-grade analytics

---