#!/usr/bin/env python3
import json
import sys
import re
from collections import Counter
from scripts.common import (
    VALID_CATEGORIES,
    VALID_SEVERITIES,
    outputs_dir, 
    normalized_dir,
)

INPUT = str(normalized_dir() / "findings.jsonl")

REQUIRED_FIELDS = [
    "finding_id",
    "tool",
    "category",
    "severity",
    "title",
    "repo",
    "branch",
    "commit_sha",
    "pipeline_id",
    "timestamp",
    "raw_ref",
    "normalized_version",
]

def main() -> None:
    errors = []
    findings = []
    seen_ids = set()

    with open(INPUT, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {idx}: invalid JSON: {e}")
                continue

            findings.append(rec)

            for field in REQUIRED_FIELDS:
                if field not in rec or rec[field] in (None, ""):
                    errors.append(f"Line {idx}: missing required field '{field}'")

            if rec.get("severity") not in VALID_SEVERITIES:
                errors.append(f"Line {idx}: invalid severity '{rec.get('severity')}'")

            if rec.get("category") not in VALID_CATEGORIES:
                errors.append(f"Line {idx}: invalid category '{rec.get('category')}'")

            fid = rec.get("finding_id")
            if fid in seen_ids:
                errors.append(f"Line {idx}: duplicate finding_id '{fid}'")
            else:
                seen_ids.add(fid)

            # Secret hygiene check
            # if rec.get("tool") == "gitleaks":
            #     desc = (rec.get("description") or "").lower()
            #     code_snippet = rec.get("code_snippet") or ""
            #     if "akia" in desc or "ghp_" in desc or "aws_secret_access_key" in desc:
            #         errors.append(f"Line {idx}: possible unmasked secret leaked in description")
            #     if "akia" in code_snippet.lower() or "ghp_" in code_snippet.lower():
            #         errors.append(f"Line {idx}: possible unmasked secret leaked in code_snippet")
            if rec.get("tool") == "gitleaks":
                desc = rec.get("description") or ""
                code_snippet = rec.get("code_snippet") or ""

                # Flag likely unmasked secrets, but allow masked forms like AKIA**** or ghp_****
                unmasked_patterns = [
                    r"AKIA[0-9A-Z]{12,}",
                    r"ghp_[A-Za-z0-9]{20,}",
                    r"AWS_SECRET_ACCESS_KEY\s*=\s*[^\s|]+",
                ]

                for pat in unmasked_patterns:
                    if re.search(pat, desc):
                        errors.append(f"Line {idx}: possible unmasked secret leaked in description")
                        break

                for pat in unmasked_patterns:
                    if re.search(pat, code_snippet):
                        errors.append(f"Line {idx}: possible unmasked secret leaked in code_snippet")
                        break

    print(f"Validated {len(findings)} findings")

    tools = Counter([f.get("tool", "unknown") for f in findings])
    severities = Counter([f.get("severity", "unknown") for f in findings])
    categories = Counter([f.get("category", "unknown") for f in findings])

    print("\nBy tool:")
    for k, v in tools.items():
        print(f"  {k}: {v}")

    print("\nBy severity:")
    for k, v in severities.items():
        print(f"  {k}: {v}")

    print("\nBy category:")
    for k, v in categories.items():
        print(f"  {k}: {v}")

    if errors:
        print("\nValidation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nValidation PASSED")

if __name__ == "__main__":
    main()