import json
import hashlib
from collections import defaultdict

INPUT = "outputs/normalized_findings.json"
OUTPUT = "outputs/correlated_findings.json"

MITRE_MAP = {
    "T1552": {
        "technique": "T1552",
        "name": "Unsecured Credentials",
        "subtechnique_examples": ["Credentials In Files", "Cloud Instance Metadata API", "Bash History"]
    }
}

def stable_finding_id(f):
    raw = f"{f.get('scanner')}|{f.get('file_path')}|{f.get('line_start')}|{f.get('rule_id')}|{f.get('mitre_technique')}"
    return hashlib.sha256(raw.encode()).hexdigest()

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    grouped = defaultdict(list)
    for finding in data["findings"]:
        key = (finding.get("file_path"), finding.get("line_start"), finding.get("mitre_technique"))
        grouped[key].append(finding)

    correlated = []
    for _, items in grouped.items():
        first = items[0]
        scanners = sorted({x["scanner"] for x in items})
        confidence = "high" if len(scanners) >= 2 else "medium"

        enriched = {
            "finding_id": stable_finding_id(first),
            "repo": data["repo"],
            "branch": data["branch"],
            "commit_sha": data["commit_sha"],
            "pipeline_id": data["pipeline_id"],
            "file_path": first["file_path"],
            "line_start": first["line_start"],
            "line_end": first["line_end"],
            "title": first["title"],
            "severity": first["severity"],
            "mitre": MITRE_MAP.get(first["mitre_technique"], {}),
            "matched_by": scanners,
            "confidence": confidence,
            "evidence_count": len(items),
            "evidence": items,
        }
        correlated.append(enriched)

    out = {
        "repo": data["repo"],
        "pipeline_id": data["pipeline_id"],
        "correlated_findings": correlated
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Correlated {len(correlated)} findings")

if __name__ == "__main__":
    main()