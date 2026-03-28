CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_first_last_seen_v` AS
SELECT
  finding_id,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(category) AS category,
  ANY_VALUE(severity) AS severity,
  ANY_VALUE(tool) AS tool,
  MIN(loaded_at) AS first_seen_at,
  MAX(loaded_at) AS last_seen_at,
  DATE(MIN(loaded_at)) AS first_seen_date,
  DATE(MAX(loaded_at)) AS last_seen_date,
  COUNT(*) AS observation_count,
  COUNT(DISTINCT pipeline_id) AS pipeline_count,
  COUNT(DISTINCT commit_sha) AS commit_count
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_observations`
GROUP BY finding_id;