CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_summary_v` AS
SELECT
  incident_id,
  repo,
  branch,
  commit_sha,
  pipeline_id,
  timestamp,
  DATE(timestamp) AS incident_date,
  title,
  summary,
  severity,
  risk_score,
  confidence,
  finding_count,
  primary_resource,
  recommended_action,
  status,
  ARRAY_LENGTH(categories) AS category_count,
  ARRAY_LENGTH(mitre_techniques) AS mitre_count,
  CASE WHEN severity = 'critical' THEN 1 ELSE 0 END AS is_critical_incident,
  CASE WHEN risk_score >= 80 THEN 1 ELSE 0 END AS is_high_risk_incident
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents`;