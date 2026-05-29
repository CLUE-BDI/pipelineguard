# DefectDojo Integration Guide

This guide details how to integrate security scan results from your CLUE-BDI repositories into **DefectDojo** (both for GitLab CI and GitHub Actions).

---

## 1. Prerequisites and Authentication

DefectDojo uses token-based authentication. Regardless of the pipeline system (GitLab or GitHub), you need:
1. **DefectDojo Server URL**: The domain/IP where DefectDojo is running (e.g., `https://dojo.sans.labs` or your custom hosted URL).
2. **DefectDojo API Key / Token**: A user token generated in DefectDojo (found under **User Profile** -> **API v2 Key**).
3. **Engagement ID**: A pre-existing target engagement inside a product in DefectDojo.

> [!TIP]
> Keep your URL and API Key safe by utilizing secrets managers (like HashiCorp Vault, GitHub Secrets, or GitLab CI Variables).

---

## 2. Option A: Integrated GitLab CI Pipeline

If you are using GitLab CI (similar to the SANS lab environments), you can include the DefectDojo component directly in your pipeline.

Add the following component inclusion to the `.gitlab-ci.yml` file of your repository (e.g., `pipelineguard` or others):

```yaml
include:
  - component: gitlab.sans.labs/operations/dm-ci-templates/defect-dojo@main
    inputs:
      tags: docker
      stage: policy
      dir: ${CI_PROJECT_DIR}/tests
      download-mr-pipeline-artifacts: true
      sarif-reports: "semgrep/*.sarif trivy-fs/*.sarif"
      trivy-reports: "trivy-scan-az/trivy.json"
      evaluate-product-grade: true
```

*Make sure your GitLab CI environment defines the `DEFECTDOJO_SERVER_URL` and `DEFECTDOJO_API_KEY` masked variables.*

---

## 3. Option B: GitHub Actions (GitHub-native workflows)

If you are running pipelines natively in GitHub Actions (such as the workflow defined in `blue-green-gateway/.github/workflows/deploy.yml`), you can upload the scan reports directly using a webhook API step.

### Step-by-Step GitHub Actions Setup

1. Store the secret token and URL in your GitHub Repository Secrets:
   - `DEFECTDOJO_URL`
   - `DEFECTDOJO_TOKEN`
   - `DEFECTDOJO_ENGAGEMENT_ID` (the specific engagement ID)

2. Update your GitHub Workflow `.github/workflows/deploy.yml` to save scan results in JSON/SARIF format and upload them:

```yaml
    # Example: Running Trivy and exporting JSON
    - name: Run Trivy Scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'config'
        format: 'json'
        output: 'trivy-report.json'
        exit-code: '0' # Don't fail the pipeline yet so we can upload findings
        severity: 'CRITICAL,HIGH'

    # Upload JSON findings to DefectDojo
    - name: Log Findings in DefectDojo
      run: |
        curl -X POST "${{ secrets.DEFECTDOJO_URL }}/api/v2/import-scan/" \
          -H "Authorization: Token ${{ secrets.DEFECTDOJO_TOKEN }}" \
          -H "Content-Type: multipart/form-data" \
          -F "file=@trivy-report.json" \
          -F "scan_type=Trivy Scan" \
          -F "engagement=${{ secrets.DEFECTDOJO_ENGAGEMENT_ID }}" \
          -F "verified=true" \
          -F "active=true" \
          -F "close_old_findings=true" \
          -F "close_old_findings_product_scope=true"
```

---

## 4. Option C: PipelineGuard Automated CLI Uploader (Recommended for Local + CI scans)

We created a custom uploader script inside the `pipelineguard` repository at [upload_to_defectdojo.py](../scripts/upload_to_defectdojo.py). It automatically processes all output scans (`trivy-fs.json`, `gitleaks.json`, `semgrep.json`, `checkov.json`) and registers them to DefectDojo.

### How to Run it

1. **Export environment variables**:
   ```bash
   export DEFECTDOJO_URL="https://dojo.example.com"
   export DEFECTDOJO_API_TOKEN="your_api_token_here"
   export DEFECTDOJO_ENGAGEMENT_ID="1"  # Replace with your engagement ID
   ```

2. **Execute the uploader**:
   ```bash
   uv run python scripts/upload_to_defectdojo.py
   ```

### Integrating with `scan_all.py`

You can call the uploader right after your local or CI execution in `pipelineguard` completes:

```bash
# Run security checks
uv run python scripts/scan_all.py

# Push results to DefectDojo
uv run python scripts/upload_to_defectdojo.py
```
