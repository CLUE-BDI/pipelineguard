CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations_summary_v` AS
SELECT
  incident_id,
  repo,
  branch,
  commit_sha,
  pipeline_id,
  loaded_at,
  DATE(loaded_at) AS load_date,
  observed_at,
  DATE(observed_at) AS observed_date,
  severity,
  risk_score,
  status,
  CASE WHEN severity = 'critical' THEN 1 ELSE 0 END AS is_critical,
  CASE WHEN severity = 'high' THEN 1 ELSE 0 END AS is_high,
  CASE WHEN risk_score >= 80 THEN 1 ELSE 0 END AS is_high_risk
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`;