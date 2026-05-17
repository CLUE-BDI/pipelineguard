#!/usr/bin/env bash

# Local directories cleanup
echo "Removing local files..."
rm -rf outputs/vulnerable-infra-project
rm -rf normalized/vulnerable-infra-project
rm -rf correlated/vulnerable-infra-project
echo "Local files removed."

# GCS Cleanup
GCS_BUCKET="pipelineguard-artifacts"
echo "Removing from GCS bucket: ${GCS_BUCKET}..."
gsutil -m rm -r "gs://${GCS_BUCKET}/raw/*/*/*/vulnerable-infra-project" 2>/dev/null || echo "No raw files to delete or deletion failed."
gsutil -m rm -r "gs://${GCS_BUCKET}/normalized/*/*/*/vulnerable-infra-project" 2>/dev/null || echo "No normalized files to delete or deletion failed."
gsutil -m rm -r "gs://${GCS_BUCKET}/correlated/*/*/*/vulnerable-infra-project" 2>/dev/null || echo "No correlated files to delete or deletion failed."

# BigQuery Cleanup
GCP_PROJECT_ID="datawarehouse-486704"
BQ_DATASET="pipelineguard_analytics"
TABLES=("findings_normalized" "incidents" "finding_observations" "incident_observations" "findings_normalized_staging" "incidents_staging")

echo "Removing from BigQuery project: ${GCP_PROJECT_ID}..."
for table in "${TABLES[@]}"; do
    echo "Deleting from ${table}..."
    bq query --use_legacy_sql=false "DELETE FROM \`${GCP_PROJECT_ID}.${BQ_DATASET}.${table}\` WHERE repo = 'vulnerable-infra-project'" || true
done

echo "Cleanup complete!"
