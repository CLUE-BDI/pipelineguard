#!/usr/bin/env python3
from scripts.common import (
    base_record,    
    load_json, 
    mask_secret,
    write_jsonl, 
    outputs_dir, 
    normalized_dir
)

INPUT_PATH = str(outputs_dir() / "gitleaks.json")
OUTPUT_PATH = str(normalized_dir() / "gitleaks.normalized.jsonl")

def main() -> None:
    raw = load_json(INPUT_PATH)
    records = []

    # Gitleaks often returns a list of findings at the top level
    findings = raw if isinstance(raw, list) else raw.get("findings", [])

    for item in findings:
        rule_id = item.get("RuleID") or item.get("ruleID") or item.get("rule_id")
        description = item.get("Description") or item.get("description") or "Potential secret detected by Gitleaks"
        file_path = item.get("File") or item.get("file") or item.get("path")
        start_line = item.get("StartLine") or item.get("startLine") or item.get("start_line") or 0
        end_line = item.get("EndLine") or item.get("endLine") or item.get("end_line") or start_line
        secret = item.get("Secret") or item.get("secret")
        match = item.get("Match") or item.get("match")

        masked = mask_secret(secret or match)
        if masked:
            normalized_description = f"{description}. Matched value masked: {masked}"
        else:
            normalized_description = description

        title = description if description else (rule_id or "Secret detected")

        rec = base_record(
            tool="gitleaks",
            category="secret",
            severity="high",
            confidence="high",
            title=title,
            description=normalized_description,
            raw_ref=INPUT_PATH,
            raw_tool="gitleaks",
            rule_id=rule_id,
            rule_name=rule_id,
            file_path=file_path,
            line_start=start_line,
            line_end=end_line,
            secret_type=rule_id,
            raw_severity=None,
            tags=["secret", "credential"],
            mitre_technique="T1552",
        )
        records.append(rec)

    write_jsonl(OUTPUT_PATH, records)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()