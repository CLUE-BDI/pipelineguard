#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from collections import Counter
from scripts.common import normalized_dir

target_name = normalized_dir().name
CORRELATED_DIR = Path("correlated") / target_name
ENRICHED_PATH = CORRELATED_DIR / "enriched_findings.jsonl"
INCIDENTS_PATH = CORRELATED_DIR / "incidents.jsonl"

VALID_SEVERITIES = {"critical", "high", "medium", "low", "info"}

INCIDENT_REQUIRED_FIELDS = [
    "incident_id",
    "repo",
    "branch",
    "commit_sha",
    "pipeline_id",
    "timestamp",
    "summary",
    "title",
    "severity",
    "risk_score",
    "related_findings",
    "finding_count",
    "recommended_action",
    "status",
]

FINDING_REQUIRED_FIELDS = [
    "finding_id",
    "tool",
    "category",
    "severity",
    "correlation_key",
    "severity_score",
    "category_score",
]


def read_jsonl(path: Path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}: line {i}: invalid JSON: {e}")
    return rows


def main():
    errors = []

    if not ENRICHED_PATH.exists():
        errors.append(f"Missing file: {ENRICHED_PATH}")
    if not INCIDENTS_PATH.exists():
        errors.append(f"Missing file: {INCIDENTS_PATH}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    enriched = read_jsonl(ENRICHED_PATH)
    incidents = read_jsonl(INCIDENTS_PATH)

    seen_incidents = set()
    severity_counts = Counter()

    for idx, rec in enumerate(enriched, start=1):
        for field in FINDING_REQUIRED_FIELDS:
            if field not in rec:
                errors.append(f"enriched line {idx}: missing field '{field}'")

        if not isinstance(rec.get("severity_score"), int):
            errors.append(f"enriched line {idx}: severity_score must be int")
        if not isinstance(rec.get("category_score"), int):
            errors.append(f"enriched line {idx}: category_score must be int")

    for idx, rec in enumerate(incidents, start=1):
        for field in INCIDENT_REQUIRED_FIELDS:
            if field not in rec:
                errors.append(f"incident line {idx}: missing field '{field}'")

        incident_id = rec.get("incident_id")
        if incident_id in seen_incidents:
            errors.append(f"incident line {idx}: duplicate incident_id '{incident_id}'")
        else:
            seen_incidents.add(incident_id)

        severity = rec.get("severity")
        if severity not in VALID_SEVERITIES:
            errors.append(f"incident line {idx}: invalid severity '{severity}'")
        else:
            severity_counts[severity] += 1

        risk_score = rec.get("risk_score")
        if not isinstance(risk_score, int):
            errors.append(f"incident line {idx}: risk_score must be int")
        elif not (0 <= risk_score <= 100):
            errors.append(f"incident line {idx}: risk_score out of range '{risk_score}'")

        related = rec.get("related_findings", [])
        if not isinstance(related, list) or len(related) == 0:
            errors.append(f"incident line {idx}: related_findings must be a non-empty list")

        finding_count = rec.get("finding_count")
        if not isinstance(finding_count, int):
            errors.append(f"incident line {idx}: finding_count must be int")
        elif isinstance(related, list) and finding_count != len(related):
            errors.append(
                f"incident line {idx}: finding_count {finding_count} does not match related_findings length {len(related)}"
            )

    print(f"Validated {len(enriched)} enriched findings")
    print(f"Validated {len(incidents)} incidents")
    print("Incident severities:")
    for sev, count in severity_counts.items():
        print(f"  {sev}: {count}")

    if errors:
        print("\nCorrelation validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nCorrelation validation PASSED")


if __name__ == "__main__":
    main()