#!/usr/bin/env python3
import json
import os
import sys
from collections import Counter
from scripts.common import normalized_dir

INPUT = str(normalized_dir() / "findings.jsonl")

MAX_CRITICAL = int(os.getenv("MAX_CRITICAL", "0"))
MAX_HIGH = int(os.getenv("MAX_HIGH", "999999"))
FAIL_ON_SECRET = os.getenv("FAIL_ON_SECRET", "true").lower() == "true"

def main() -> None:
    counts = Counter()
    secret_count = 0
    total = 0

    with open(INPUT, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            total += 1
            severity = rec.get("severity", "unknown")
            category = rec.get("category", "unknown")
            counts[severity] += 1
            if category == "secret":
                secret_count += 1

    print(f"Total findings: {total}")
    print(f"Severity counts: {dict(counts)}")
    print(f"Secret findings: {secret_count}")

    errors = []

    if counts["critical"] > MAX_CRITICAL:
        errors.append(
            f"critical findings {counts['critical']} exceeded threshold {MAX_CRITICAL}"
        )

    if counts["high"] > MAX_HIGH:
        errors.append(
            f"high findings {counts['high']} exceeded threshold {MAX_HIGH}"
        )

    if FAIL_ON_SECRET and secret_count > 0:
        errors.append(
            f"secret findings present ({secret_count}) and FAIL_ON_SECRET=true"
        )

    if errors:
        print("\nThreshold enforcement FAILED:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    print("\nThreshold enforcement PASSED")

if __name__ == "__main__":
    main()