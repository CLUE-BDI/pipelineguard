#!/usr/bin/env python3
from pathlib import Path
from scripts.common import (
    read_jsonl, 
    write_jsonl,
    outputs_dir, 
    normalized_dir,
)

INPUTS = [
    str(normalized_dir() / "gitleaks.normalized.jsonl"),
    str(normalized_dir() / "checkov.normalized.jsonl"),
    str(normalized_dir() / "semgrep.normalized.jsonl"),
    str(normalized_dir() / "trivy.normalized.jsonl"),
]


OUTPUT_PATH = str(normalized_dir() / "findings.jsonl")

def main() -> None:
    merged = []
    seen = set()

    for path in INPUTS:
        p = Path(path)
        if not p.exists():
            print(f"Skipping missing file: {path}")
            continue

        for record in read_jsonl(path):
            fid = record.get("finding_id")
            if fid in seen:
                continue
            seen.add(fid)
            merged.append(record)

    write_jsonl(OUTPUT_PATH, merged)
    print(f"Wrote {len(merged)} merged findings to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()