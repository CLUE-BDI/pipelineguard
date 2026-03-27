#!/usr/bin/env python3
import json
import hashlib
from collections import defaultdict
from pathlib import Path
from scripts.common import normalized_dir, utc_now

TARGET = Path(normalized_dir().name)
INPUT_PATH = normalized_dir() / "findings.jsonl"
CORRELATED_DIR = Path("correlated") / normalized_dir().name
ENRICHED_PATH = CORRELATED_DIR / "enriched_findings.jsonl"
INCIDENTS_PATH = CORRELATED_DIR / "incidents.jsonl"

SEVERITY_WEIGHTS_PATH = Path("mappings") / "severity_weights.json"
CATEGORY_WEIGHTS_PATH = Path("mappings") / "category_weights.json"
MITRE_MAP_PATH = Path("mappings") / "mitre_map.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_incident_id(repo: str, correlation_key: str) -> str:
    raw = f"{repo}|{correlation_key}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"inc_{digest}"


def infer_correlation_key(finding: dict) -> str:
    for field in ("resource_name", "file_path", "package_name"):
        value = finding.get(field)
        if value:
            return f"{field}:{value}"

    category = finding.get("category", "unknown")
    mitre = finding.get("mitre_technique") or "no-mitre"
    rule_id = finding.get("rule_id") or "no-rule"
    return f"fallback:{category}:{mitre}:{rule_id}"


def severity_rank(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    if score >= 10:
        return "low"
    return "info"


def main():
    findings = load_jsonl(INPUT_PATH)
    severity_weights = load_json(SEVERITY_WEIGHTS_PATH)
    category_weights = load_json(CATEGORY_WEIGHTS_PATH)
    mitre_map = load_json(MITRE_MAP_PATH)

    enriched = []

    for finding in findings:
        tool = finding.get("tool", "")
        rule_id = finding.get("rule_id", "")
        map_key = f"{tool}:{rule_id}"

        if not finding.get("mitre_technique"):
            finding["mitre_technique"] = mitre_map.get(map_key)

        sev = finding.get("severity", "unknown")
        cat = finding.get("category", "unknown")

        finding["severity_score"] = severity_weights.get(sev, 0)
        finding["category_score"] = category_weights.get(cat, 0)
        finding["correlation_key"] = infer_correlation_key(finding)

        enriched.append(finding)

    groups = defaultdict(list)
    for finding in enriched:
        groups[finding["correlation_key"]].append(finding)

    incidents = []

    for correlation_key, members in groups.items():
        repo = members[0]["repo"]
        branch = members[0]["branch"]
        commit_sha = members[0]["commit_sha"]
        pipeline_id = members[0]["pipeline_id"]

        categories = sorted({m.get("category", "unknown") for m in members})
        mitre_techniques = sorted({m.get("mitre_technique") for m in members if m.get("mitre_technique")})
        related_findings = [m["finding_id"] for m in members]

        score = sum(m.get("severity_score", 0) + m.get("category_score", 0) for m in members)

        # simple escalation rules
        if "secret" in categories and ("k8s_misconfiguration" in categories or "iac_misconfiguration" in categories):
            score += 20
        if "secret" in categories and "container_risk" in categories:
            score += 20
        if "vulnerability" in categories and "container_risk" in categories:
            score += 15

        score = min(score, 100)
        severity = severity_rank(score)

        primary_resource = (
            members[0].get("resource_name")
            or members[0].get("file_path")
            or members[0].get("package_name")
            or correlation_key
        )

        if "secret" in categories:
            recommended_action = "Block release and rotate exposed credentials"
            title = "Credential exposure detected"
        elif "vulnerability" in categories and "container_risk" in categories:
            recommended_action = "Patch vulnerable dependency or image before release"
            title = "Container vulnerability and risk combination detected"
        elif "k8s_misconfiguration" in categories:
            recommended_action = "Review Kubernetes security context and deployment settings"
            title = "Kubernetes misconfiguration detected"
        else:
            recommended_action = "Review findings and remediate before release"
            title = "Correlated security findings detected"

        summary = f"{len(members)} related findings grouped under {correlation_key}"

        incident = {
            "incident_id": build_incident_id(repo, correlation_key),
            "repo": repo,
            "branch": branch,
            "commit_sha": commit_sha,
            "pipeline_id": pipeline_id,
            "timestamp": utc_now(),
            "summary": summary,
            "title": title,
            "severity": severity,
            "risk_score": score,
            "confidence": "medium" if len(members) == 1 else "high",
            "categories": categories,
            "mitre_techniques": mitre_techniques,
            "related_findings": related_findings,
            "finding_count": len(members),
            "primary_resource": primary_resource,
            "recommended_action": recommended_action,
            "status": "open",
            "normalized_version": "v1",
        }
        incidents.append(incident)

    write_jsonl(ENRICHED_PATH, enriched)
    write_jsonl(INCIDENTS_PATH, incidents)

    print(f"Wrote {len(enriched)} enriched findings to {ENRICHED_PATH}")
    print(f"Wrote {len(incidents)} incidents to {INCIDENTS_PATH}")


if __name__ == "__main__":
    main()