CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_observations_summary_v` AS
SELECT
  finding_id,
  repo,
  branch,
  commit_sha,
  pipeline_id,
  loaded_at,
  DATE(loaded_at) AS load_date,
  observed_at,
  DATE(observed_at) AS observed_date,
  severity,
  category,
  tool,
  status,
  CASE WHEN category = 'secret' THEN 1 ELSE 0 END AS is_secret,
  CASE WHEN severity = 'critical' THEN 1 ELSE 0 END AS is_critical,
  CASE WHEN severity = 'high' THEN 1 ELSE 0 END AS is_high
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_observations`;