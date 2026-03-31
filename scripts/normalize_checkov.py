#!/usr/bin/env python3
from scripts.common import (
    base_record,
    infer_category_from_path,
    load_json,
    normalize_severity,
    to_int,
    write_jsonl,
    outputs_dir,
    normalized_dir,
)

from pathlib import Path


INPUT_PATH = str(outputs_dir() / "checkov.json")
OUTPUT_PATH = str(normalized_dir() / "checkov.normalized.jsonl")

CHECKOV_SEVERITY_OVERRIDES = {
    "CKV_AWS_24": "high",
    "CKV_K8S_20": "high",
    "CKV_K8S_22": "medium",
}


def parse_line_range(line_range):
    if not line_range:
        return 0, 0

    if isinstance(line_range, list):
        if len(line_range) >= 2:
            return to_int(line_range[0]), to_int(line_range[1])
        if len(line_range) == 1:
            x = to_int(line_range[0])
            return x, x

    return 0, 0


def extract_failed_checks(raw):
    # Shape 1: {"results": {"failed_checks": [...]}}
    if isinstance(raw, dict):
        return raw.get("results", {}).get("failed_checks", [])

    # Shape 2: [ {"results": {"failed_checks": [...]}} ]
    if isinstance(raw, list):
        failed = []

        for entry in raw:
            if not isinstance(entry, dict):
                continue

            # nested report object
            if "results" in entry:
                failed.extend(entry.get("results", {}).get("failed_checks", []))
            # already a failed-check item
            elif "check_id" in entry or "check_name" in entry:
                failed.append(entry)

        return failed

    raise TypeError(f"Unsupported Checkov JSON type: {type(raw).__name__}")


def main() -> None:
    if not Path(INPUT_PATH).exists():
        write_jsonl(OUTPUT_PATH, [])
        print(f"[checkov] Input missing, wrote 0 records to {OUTPUT_PATH}")
        return

    raw = load_json(INPUT_PATH)
    failed_checks = extract_failed_checks(raw)
    records = []

    for item in failed_checks:
        if not isinstance(item, dict):
            continue

        rule_id = item.get("check_id")
        title = item.get("check_name") or rule_id or "Checkov finding"
        file_path = item.get("file_path") or item.get("file_abs_path")
        resource_name = item.get("resource")
        guideline = item.get("guideline")
        category = infer_category_from_path(file_path)
        # severity = normalize_severity(item.get("severity"), default="medium")

        raw_sev = item.get("severity")
        severity = normalize_severity(
            raw_sev or CHECKOV_SEVERITY_OVERRIDES.get(rule_id),
            default="medium",
        )

        start_line, end_line = parse_line_range(item.get("file_line_range"))

        description_parts = [title]
        if guideline:
            description_parts.append(f"Guideline: {guideline}")
        description = " | ".join(description_parts)

        tool_finding_id = "|".join(
            [
                rule_id or "",
                resource_name or "",
                file_path or "",
                str(start_line),
                str(end_line),
            ]
        )

        rec = base_record(
            tool="checkov",
            category=category,
            severity=severity,
            confidence="medium",
            title=title,
            description=description,
            raw_ref=INPUT_PATH,
            raw_tool="checkov",
            rule_id=rule_id,
            rule_name=title,
            tool_finding_id=tool_finding_id,
            file_path=file_path,
            line_start=start_line,
            line_end=end_line,
            resource_type="terraform_resource" if category == "iac_misconfiguration" else "k8s_resource",
            resource_name=resource_name,
            recommendation=guideline,
            raw_severity=item.get("severity"),
            references=[guideline] if guideline else [],
            tags=["iac"] if category == "iac_misconfiguration" else ["k8s"],
        )
        records.append(rec)

    write_jsonl(OUTPUT_PATH, records)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()