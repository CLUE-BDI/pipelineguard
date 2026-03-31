#!/usr/bin/env python3
from scripts.common import (
    base_record,
    load_json, 
    normalize_severity,
    write_jsonl, 
    outputs_dir, 
    normalized_dir,
)

from pathlib import Path

INPUT_PATH = str(outputs_dir() / "semgrep.json")
OUTPUT_PATH = str(normalized_dir() / "semgrep.normalized.jsonl")

def infer_subcategory(check_id: str, message: str) -> str | None:
    text = f"{check_id} {message}".lower()
    if "subprocess" in text or "shell=true" in text or "shell execution" in text:
        return "command_injection"
    if "hardcoded" in text or "password" in text or "secret" in text:
        return "hardcoded_credential"
    if "eval" in text:
        return "unsafe_eval"
    return None

def infer_mitre(check_id: str, message: str) -> str | None:
    text = f"{check_id} {message}".lower()
    if "subprocess" in text or "shell" in text:
        return "T1059"
    if "hardcoded" in text or "secret" in text:
        return "T1552"
    return None

def main() -> None:
    if not Path(INPUT_PATH).exists():
        write_jsonl(OUTPUT_PATH, [])
        print(f"[semgrep] Input missing, wrote 0 records to {OUTPUT_PATH}")
        return

    raw = load_json(INPUT_PATH)
    findings = raw.get("results", [])
    records = []

    for item in findings:
        check_id = item.get("check_id")
        path = item.get("path")
        start = item.get("start", {}) or {}
        end = item.get("end", {}) or {}
        extra = item.get("extra", {}) or {}

        message = extra.get("message") or "Semgrep finding"
        raw_sev = extra.get("severity")
        severity = normalize_severity(raw_sev, default="medium")
        code_snippet = extra.get("lines")

        subcategory = infer_subcategory(check_id or "", message)
        mitre = infer_mitre(check_id or "", message)

        rec = base_record(
            tool="semgrep",
            category="code_issue",
            severity=severity,
            confidence="medium",
            title=check_id or "Semgrep finding",
            description=message,
            raw_ref=INPUT_PATH,
            raw_tool="semgrep",
            rule_id=check_id,
            rule_name=check_id,
            file_path=path,
            line_start=start.get("line", 0),
            line_end=end.get("line", 0),
            code_snippet=code_snippet,
            resource_type="source_file",
            resource_name=path,
            subcategory=subcategory,
            raw_severity=raw_sev,
            tags=["code", "sast"],
            mitre_technique=mitre,
        )
        records.append(rec)

    write_jsonl(OUTPUT_PATH, records)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()