#!/usr/bin/env python3
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

TARGET_REPO_NAME = os.getenv("TARGET_REPO_NAME")
if not TARGET_REPO_NAME:
    raise RuntimeError(
        "TARGET_REPO_NAME is not set. Run 'source config/target.env' before running Phase 2 scripts."
    )

def outputs_dir() -> Path:
    return Path("outputs") / TARGET_REPO_NAME

def normalized_dir() -> Path:
    return Path("normalized") / TARGET_REPO_NAME

DEFAULT_METADATA = {
    "repo": os.getenv("PG_REPO", TARGET_REPO_NAME),
    "branch": os.getenv("PG_BRANCH", "main"),
    "commit_sha": os.getenv("PG_COMMIT_SHA", "local-dev"),
    "pipeline_id": os.getenv("PG_PIPELINE_ID", "phase2-local"),
    "environment": os.getenv("PG_ENVIRONMENT", "local"),
}

VALID_SEVERITIES = {"critical", "high", "medium", "low", "info", "unknown"}
VALID_CATEGORIES = {
    "secret",
    "vulnerability",
    "iac_misconfiguration",
    "k8s_misconfiguration",
    "code_issue",
    "dependency_risk",
    "supply_chain",
    "container_risk",
    "policy_violation",
    "unknown",
}

SEVERITY_MAP = {
    "CRITICAL": "critical",
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
    "INFO": "info",
    "WARNING": "medium",
    "WARN": "medium",
    "ERROR": "high",
    "UNKNOWN": "unknown",
    "": "unknown",
    None: "unknown",
}

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def write_jsonl(path: str, records: Iterable[Dict[str, Any]]) -> None:
    records_list = list(records)
    if not records_list:
        return
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        for r in records_list:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def normalize_severity(raw: Optional[str], default: str = "unknown") -> str:
    sev = SEVERITY_MAP.get((raw or "").upper(), None)
    if sev:
        return sev
    if default in VALID_SEVERITIES:
        return default
    return "unknown"

def infer_category_from_path(path: Optional[str]) -> str:
    if not path:
        return "unknown"
    p = path.lower()
    if p.endswith(".tf") or "/infra/" in p or p.startswith("infra/"):
        return "iac_misconfiguration"
    if "k8s/" in p or p.endswith(".yaml") or p.endswith(".yml"):
        return "k8s_misconfiguration"
    if p.endswith("dockerfile") or "docker/" in p:
        return "container_risk"
    return "unknown"

def mask_secret(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    if len(value) <= 4:
        return "*" * len(value)
    return value[:4] + "*" * (len(value) - 4)

def to_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def build_finding_id(
    tool: str,
    rule_id: Optional[str],
    file_path: Optional[str],
    line_start: Any,
    title: str,
    resource_name: Optional[str] = None,
    vulnerability_id: Optional[str] = None,
    package_name: Optional[str] = None,
) -> str:
    base = "|".join([
        tool or "",
        rule_id or "",
        file_path or "",
        str(to_int(line_start)),
        title or "",
        resource_name or "",
        vulnerability_id or "",
        package_name or "",
    ])
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]
    return f"f_{digest}"

def base_record(
    *,
    tool: str,
    category: str,
    severity: str,
    confidence: str,
    title: str,
    description: str,
    raw_ref: str,
    raw_tool: str,
    rule_id: Optional[str] = None,
    rule_name: Optional[str] = None,
    tool_finding_id: Optional[str] = None,
    subcategory: Optional[str] = None,
    recommendation: Optional[str] = None,
    file_path: Optional[str] = None,
    line_start: int = 0,
    line_end: int = 0,
    code_snippet: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_name: Optional[str] = None,
    resource_namespace: Optional[str] = None,
    package_name: Optional[str] = None,
    installed_version: Optional[str] = None,
    fixed_version: Optional[str] = None,
    secret_type: Optional[str] = None,
    vulnerability_id: Optional[str] = None,
    raw_severity: Optional[str] = None,
    tags: Optional[List[str]] = None,
    references: Optional[List[str]] = None,
    mitre_technique: Optional[str] = None,
    compliance_controls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    rec = {
        "finding_id": build_finding_id(
            tool,
            rule_id,
            file_path,
            line_start,
            title,
            resource_name=resource_name,
            vulnerability_id=vulnerability_id,
            package_name=package_name,
        ),
        "tool": tool,
        "tool_finding_id": tool_finding_id,
        "category": category if category in VALID_CATEGORIES else "unknown",
        "subcategory": subcategory,
        "severity": severity if severity in VALID_SEVERITIES else "unknown",
        "confidence": confidence,
        "title": title,
        "description": description,
        "recommendation": recommendation,
        "rule_id": rule_id,
        "rule_name": rule_name,
        "file_path": file_path,
        "line_start": to_int(line_start),
        "line_end": to_int(line_end),
        "code_snippet": code_snippet,
        "resource_type": resource_type,
        "resource_name": resource_name,
        "resource_namespace": resource_namespace,
        "package_name": package_name,
        "installed_version": installed_version,
        "fixed_version": fixed_version,
        "secret_type": secret_type,
        "vulnerability_id": vulnerability_id,
        "repo": DEFAULT_METADATA["repo"],
        "branch": DEFAULT_METADATA["branch"],
        "commit_sha": DEFAULT_METADATA["commit_sha"],
        "pipeline_id": DEFAULT_METADATA["pipeline_id"],
        "scanner_stage": "security_scanners",
        "timestamp": utc_now(),
        "status": "open",
        "environment": DEFAULT_METADATA["environment"],
        "raw_ref": raw_ref,
        "raw_tool": raw_tool,
        "raw_severity": raw_severity,
        "normalized_version": "v1",
        "tags": tags or [],
        "references": references or [],
        "mitre_technique": mitre_technique,
        "compliance_controls": compliance_controls or [],
    }
    return rec