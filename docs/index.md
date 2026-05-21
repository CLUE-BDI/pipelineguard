# PipelineGuard Documentation

Welcome to the official developer and deployment documentation for the **PipelineGuard** project.

PipelineGuard is a secure multi-cloud data engineering platform built to ingest, normalize, and analyze security telemetry (from scanners like Trivy, Gitleaks, Checkov, and Semgrep) at scale. It transforms unstructured findings into standardized schemas, stores them in a Google Cloud Storage (GCS) data lake, and ingests them into Google BigQuery for compliance reporting and Looker Studio visualizations.

## Documentation Structure

This documentation site is split into the following sections tailored for developers and analytics engineers:

*   [**Development & Setup Guide**](dev_guide.md): Instructions for local system requirements, python virtual environment setup (`uv`), local script executions, and running pipelines.
*   [**Deployment Guide**](deploy_guide.md): Details on configuring GCP credentials, creating Google Cloud Storage buckets, setting up BigQuery tables/views, and integrating with GitLab CI/CD.

---

### Core Tech Stack Summary
*   **Core Engine**: Python 3.13, Pandas, Pydantic, Astral `uv`
*   **Infrastructure**: Google Cloud Platform (GCS, BigQuery), Docker
*   **Scanners Integrated**: Checkov, Trivy, Gitleaks, Semgrep
*   **CI/CD**: GitLab CI/CD pipelines
*   **Reporting**: Google Looker Studio
