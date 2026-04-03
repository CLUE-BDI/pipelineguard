# 🚀 PipelineGuard — Multi-Cloud DevSecOps Analytics Platform

## 📌 Overview

**PipelineGuard** is a multi-cloud DevSecOps analytics platform designed to:

* Detect vulnerabilities across CI/CD pipelines
* Normalize and correlate findings across multiple security tools
* Map findings to MITRE ATT&CK techniques
* Store and analyze results in a scalable data platform
* Provide actionable insights via dashboards

It integrates scanning, data engineering, and analytics into a unified pipeline across **AWS, Azure, and GCP**.

---

## 🏗️ Architecture

The platform is designed using a **multi-cloud execution + centralized data model**:

* **Local Docker** → Development & testing
* **AWS ECS (Fargate)** → Batch scanning & scheduled execution
* **Azure AKS** → API, workers, and platform services
* **GCP (GCS + BigQuery)** → Central analytics and storage

### 🔁 High-Level Flow

```
Developer → CI/CD → Containers → Scan → Normalize → Correlate
         → GCS → BigQuery → Views → Dashboard
```

---

## 🧱 Core Components

### 🔹 1. Scanner Layer (Phase 1)

Runs security tools against target repositories:

* Gitleaks (secrets)
* Trivy (containers + dependencies)
* Checkov (IaC)
* Semgrep (code)

📦 Container: `pipelineguard-scanners`

---

### 🔹 2. Normalization Layer (Phase 2)

Standardizes outputs into a unified schema:

* JSONL format
* Common severity model
* Deterministic finding IDs

📦 Container: `pipelineguard-runtime`

---

### 🔹 3. Correlation Engine (Phase 5)

* Groups findings into incidents
* Maps to **MITRE ATT&CK**
* Calculates risk scores
* Deduplicates overlapping signals

---

### 🔹 4. Data Platform (GCP)

#### Storage

* **GCS Bucket**: `pipelineguard-artifacts`

  * raw/
  * normalized/
  * correlated/

#### Analytics

* **BigQuery Dataset**: `pipelineguard_analytics`

Tables:

* `findings_normalized`
* `incidents`
* `correlated_findings`

Views:

* 24 analytical views (MITRE, severity, trends, risk)

Dashboard:

* **Looker Studio**

---

## ☁️ Multi-Cloud Deployment

### 🟠 AWS (ECS Fargate)

* Batch scan execution
* Scheduled runs via EventBridge
* Blue/Green deployment via CodeDeploy
* Container registry: ECR

---

### 🔵 Azure (AKS)

* API services (FastAPI)
* Background workers
* Blue/Green cluster strategy
* Container registry: ACR

---

### 🟢 GCP

* GCS for artifact storage
* BigQuery for analytics
* Looker Studio for visualization

---

## 🔄 Blue/Green Deployment Strategy

### AWS ECS

* Two environments: **BLUE / GREEN**
* Managed by **CodeDeploy**
* Traffic shifted via ALB

### Azure AKS

* Two clusters: **AKS-BLUE / AKS-GREEN**
* Traffic managed via:

  * Azure Front Door / App Gateway / DNS
* Zero-downtime deployments

---

## 🐳 Containerization

### Images

| Image                    | Purpose                        |
| ------------------------ | ------------------------------ |
| `pipelineguard-scanners` | Security scanning tools        |
| `pipelineguard-runtime`  | Normalize, correlate, validate |
| `gcp-jobs` (optional)    | BigQuery + GCS operations      |

---

## ⚙️ CI/CD Pipeline

Implemented using **GitLab CI/CD**

### Stages

1. **Build**
2. **Scan**
3. **Normalize**
4. **Correlate**
5. **Validate**
6. **Publish Artifacts**
7. **Load to BigQuery**
8. **Apply Views**
9. **Deploy (AWS + Azure)**

---

## 🗂️ Repository Structure

```
pipelineguard/
│
├── scripts/
│   ├── run_phase1.sh
│   ├── run_phase2.sh
│   ├── normalize_*.py
│   ├── correlate_findings.py
│   ├── validate_findings.py
│   └── validate_correlation.py
│
├── sql/
│   └── views/
│       ├── 01_incident_categories_v.sql
│       ├── ...
│       └── 24_*.sql
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
    ├── modules/
    └── environments/
```

---

## 🛠️ Local Development

### Build containers

```bash
docker build -f Dockerfile.scanners -t pipelineguard-scanners .
docker build -f Dockerfile.runtime -t pipelineguard-runtime .
```

### Run scanning

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  -e TARGET_REPO_NAME=terragoat \
  -e TARGET_REPO_PATH=/app/vulnerable-repos/terragoat \
  pipelineguard-scanners \
  bash -lc './scripts/run_phase1.sh'
```

### Run normalization & correlation

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  -e TARGET_REPO_NAME=terragoat \
  pipelineguard-runtime \
  bash -lc './scripts/run_phase2.sh && uv run python -m scripts.correlate_findings'
```

---

## 📊 Data Flow

```
Scanners → JSON → Normalized JSONL → Correlated JSONL
        → GCS → BigQuery → Views → Dashboard
```

---

## 🔐 Security & Secrets

* AWS: Secrets Manager
* Azure: Key Vault
* GCP: Service Account

Environment variable:

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

---

## 📈 Future Enhancements

* Real-time streaming (Kafka / Kinesis)
* Automated remediation (Lambda / Functions)
* ML-based risk scoring
* SBOM integration (Syft/Grype)
* Policy engine (OPA/Rego)

---

## 🎯 Key Features

* Multi-cloud execution
* Unified vulnerability schema
* MITRE ATT&CK mapping
* Risk-based prioritization
* Scalable analytics with BigQuery
* Blue/Green zero-downtime deployment

---

## 👤 Author

**Md Hasan**
Cloud Platform Security | DevSecOps | Data Engineering

---

## 📄 License

MIT License (or specify as needed)

---

## ⭐ Summary

PipelineGuard combines:

* DevSecOps scanning
* Data engineering pipelines
* Multi-cloud deployment
* Advanced analytics

into a **single, production-grade security intelligence platform**.

---
