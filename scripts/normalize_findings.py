import json
import os
from datetime import datetime, timezone

OUTPUT_DIR = "outputs"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return default

def normalize_gitleaks(data):
    findings = []
    for item in data if isinstance(data, list) else []:
        findings.append({
            "scanner": "gitleaks",
            "rule_id": item.get("RuleID"),
            "title": item.get("Description", "Secret detected"),
            "severity": "high",
            "file_path": item.get("File"),
            "line_start": item.get("StartLine"),
            "line_end": item.get("EndLine"),
            "secret_type": item.get("Tags", []),
            "match": item.get("Match"),
            "mitre_technique": "T1552",
            "raw": item,
        })
    return findings

def normalize_trivy(data):
    findings = []
    for result in data.get("Results", []):
        for secret in result.get("Secrets", []):
            findings.append({
                "scanner": "trivy",
                "rule_id": secret.get("RuleID"),
                "title": secret.get("Title", "Secret detected"),
                "severity": secret.get("Severity", "HIGH").lower(),
                "file_path": secret.get("Target") or result.get("Target"),
                "line_start": secret.get("StartLine"),
                "line_end": secret.get("EndLine"),
                "secret_type": secret.get("Category"),
                "match": secret.get("Match"),
                "mitre_technique": "T1552",
                "raw": secret,
            })
    return findings

def normalize_checkov(data):
    findings = []
    if isinstance(data, list):
        docs = data
    else:
        docs = [data]

    for doc in docs:
        results = doc.get("results", {})
        failed_checks = results.get("failed_checks", [])
        for item in failed_checks:
            findings.append({
                "scanner": "checkov",
                "rule_id": item.get("check_id"),
                "title": item.get("check_name"),
                "severity": "medium",
                "file_path": item.get("file_path"),
                "line_start": item.get("file_line_range", [None])[0],
                "line_end": item.get("file_line_range", [None, None])[-1],
                "secret_type": "config/plaintext-secret",
                "match": item.get("code_block"),
                "mitre_technique": "T1552",
                "raw": item,
            })
    return findings

def normalize_semgrep(data):
    findings = []
    for item in data.get("results", []):
        findings.append({
            "scanner": "semgrep",
            "rule_id": item.get("check_id"),
            "title": item.get("extra", {}).get("message", "Semgrep finding"),
            "severity": item.get("extra", {}).get("severity", "ERROR").lower(),
            "file_path": item.get("path"),
            "line_start": item.get("start", {}).get("line"),
            "line_end": item.get("end", {}).get("line"),
            "secret_type": "pattern/plaintext-secret",
            "match": item.get("extra", {}).get("lines"),
            "mitre_technique": item.get("extra", {}).get("metadata", {}).get("mitre", {}).get("technique", "T1552"),
            "raw": item,
        })
    return findings

def main():
    normalized = {
        "repo": os.getenv("CI_PROJECT_PATH", "local/pipelineguard-demo"),
        "branch": os.getenv("CI_COMMIT_REF_NAME", "local"),
        "commit_sha": os.getenv("CI_COMMIT_SHA", "dev-local"),
        "pipeline_id": os.getenv("CI_PIPELINE_ID", "local-run"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "findings": [],
    }

    normalized["findings"].extend(normalize_gitleaks(load_json(f"{OUTPUT_DIR}/gitleaks.json", [])))
    normalized["findings"].extend(normalize_trivy(load_json(f"{OUTPUT_DIR}/trivy.json", {})))
    normalized["findings"].extend(normalize_checkov(load_json(f"{OUTPUT_DIR}/checkov.json", {})))
    normalized["findings"].extend(normalize_semgrep(load_json(f"{OUTPUT_DIR}/semgrep.json", {})))

    with open(f"{OUTPUT_DIR}/normalized_findings.json", "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2)

    print(f"Wrote {len(normalized['findings'])} normalized findings")

if __name__ == "__main__":
    main()