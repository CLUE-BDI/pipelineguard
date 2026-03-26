#!/usr/bin/env python3
from pathlib import Path
from scripts.common import (
    base_record,
    infer_category_from_path,
    load_json, 
    normalize_severity,
    write_jsonl, 
    outputs_dir, 
    normalized_dir,
)

FS_INPUT = str(outputs_dir() / "trivy-fs.json")
CONFIG_INPUT = str(outputs_dir() / "trivy-config.json")
OUTPUT_PATH = str(normalized_dir() / "trivy.normalized.jsonl")


def normalize_vulnerabilities(raw_path: str):
    raw = load_json(raw_path)
    records = []

    for result in raw.get("Results", []):
        target = result.get("Target")
        vulns = result.get("Vulnerabilities") or []

        for vuln in vulns:
            vuln_id = vuln.get("VulnerabilityID")
            title = vuln.get("Title") or vuln_id or "Trivy vulnerability"
            desc = vuln.get("Description") or title
            sev = vuln.get("Severity")
            primary_url = vuln.get("PrimaryURL")

            rec = base_record(
                tool="trivy",
                category="vulnerability",
                subcategory="dependency_vulnerability",
                severity=normalize_severity(sev, default="unknown"),
                confidence="high",
                title=title,
                description=desc,
                raw_ref=raw_path,
                raw_tool="trivy",
                rule_id=vuln_id,
                rule_name=vuln_id,
                vulnerability_id=vuln_id,
                package_name=vuln.get("PkgName"),
                installed_version=vuln.get("InstalledVersion"),
                fixed_version=vuln.get("FixedVersion"),
                resource_type=result.get("Type") or "filesystem_target",
                resource_name=target,
                raw_severity=sev,
                references=[primary_url] if primary_url else [],
                tags=["dependency", "vuln"],
            )
            records.append(rec)

    return records

def normalize_misconfigurations(raw_path: str):
    raw = load_json(raw_path)
    records = []

    for result in raw.get("Results", []):
        target = result.get("Target")
        misconfigs = result.get("Misconfigurations") or []

        for mc in misconfigs:
            rule_id = mc.get("ID")
            title = mc.get("Title") or rule_id or "Trivy misconfiguration"
            desc = mc.get("Description") or title
            sev = mc.get("Severity")
            resolution = mc.get("Resolution")
            primary_url = mc.get("PrimaryURL")

            category = infer_category_from_path(target)
            if category == "unknown" and target:
                t = str(target).lower()
                if "dockerfile" in t:
                    category = "container_risk"

            rec = base_record(
                tool="trivy",
                category=category,
                severity=normalize_severity(sev, default="medium"),
                confidence="medium",
                title=title,
                description=desc,
                recommendation=resolution,
                raw_ref=raw_path,
                raw_tool="trivy",
                rule_id=rule_id,
                rule_name=title,
                file_path=target,
                resource_type="config_file",
                resource_name=Path(target).name if target else None,
                raw_severity=sev,
                references=[primary_url] if primary_url else [],
                tags=["config", "misconfiguration"],
            )
            records.append(rec)

    return records

def main() -> None:
    all_records = []

    if Path(FS_INPUT).exists():
        all_records.extend(normalize_vulnerabilities(FS_INPUT))

    if Path(CONFIG_INPUT).exists():
        all_records.extend(normalize_misconfigurations(CONFIG_INPUT))

    write_jsonl(OUTPUT_PATH, all_records)
    print(f"Wrote {len(all_records)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()