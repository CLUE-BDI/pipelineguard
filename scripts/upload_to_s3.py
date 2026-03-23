import boto3
import os

BUCKET = os.getenv("PIPELINEGUARD_RAW_BUCKET", "pipelineguard-raw-artifacts")
s3 = boto3.client("s3")

FILES = [
    "outputs/gitleaks.json",
    "outputs/trivy.json",
    "outputs/checkov.json",
    "outputs/semgrep.json",
    "outputs/normalized_findings.json",
    "outputs/correlated_findings.json",
]

def main():
    for path in FILES:
        if os.path.exists(path):
            key = f"scan-artifacts/{os.path.basename(path)}"
            s3.upload_file(path, BUCKET, key)
            print(f"Uploaded {path} to s3://{BUCKET}/{key}")

if __name__ == "__main__":
    main()