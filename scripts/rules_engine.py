import json
import os
import requests
import sys

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
JIRA_URL = os.getenv("JIRA_URL", "")
JIRA_USER = os.getenv("JIRA_USER", "")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")
JIRA_PROJECT = os.getenv("JIRA_PROJECT", "SEC")

def send_slack(text):
    if not SLACK_WEBHOOK:
        print("Slack not configured")
        return
    requests.post(SLACK_WEBHOOK, json={"text": text}, timeout=10)

def create_jira(summary, description):
    if not all([JIRA_URL, JIRA_USER, JIRA_TOKEN]):
        print("Jira not configured")
        return
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"}
        }
    }
    r = requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        json=payload,
        auth=(JIRA_USER, JIRA_TOKEN),
        headers={"Content-Type": "application/json"},
        timeout=15
    )
    print("Jira status:", r.status_code, r.text)

def main():
    with open("outputs/correlated_findings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    block_release = False

    for finding in data["correlated_findings"]:
        if finding["mitre"]["technique"] == "T1552":
            scanners = ", ".join(finding["matched_by"])
            text = (
                f"[PipelineGuard] T1552 detected in {finding['repo']}\n"
                f"File: {finding['file_path']}:{finding['line_start']}\n"
                f"Confidence: {finding['confidence']}\n"
                f"Matched by: {scanners}"
            )
            send_slack(text)

            create_jira(
                summary=f"T1552 plaintext credentials in {finding['repo']}",
                description=text
            )

            if finding["confidence"] == "high":
                block_release = True

    if block_release:
        print("Blocking release due to high-confidence T1552 finding")
        sys.exit(1)

    print("No blocking findings")

if __name__ == "__main__":
    main()