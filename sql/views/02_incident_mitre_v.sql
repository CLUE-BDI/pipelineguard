CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_mitre_v` AS
SELECT
  incident_id,
  repo,
  branch,
  commit_sha,
  pipeline_id,
  timestamp,
  DATE(timestamp) AS incident_date,
  severity,
  risk_score,
  title,
  recommended_action,
  status,
  mitre_technique
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents`,
UNNEST(JSON_EXTRACT_STRING_ARRAY(mitre_techniques)) AS mitre_technique;