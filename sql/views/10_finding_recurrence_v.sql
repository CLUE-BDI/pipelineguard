CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_recurrence_v` AS
SELECT
  finding_id,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(category) AS category,
  ANY_VALUE(severity) AS severity,
  ANY_VALUE(tool) AS tool,
  COUNT(*) AS observation_count,
  COUNT(DISTINCT pipeline_id) AS pipeline_count,
  COUNT(DISTINCT commit_sha) AS commit_count,
  MIN(loaded_at) AS first_seen_at,
  MAX(loaded_at) AS last_seen_at,
  TIMESTAMP_DIFF(MAX(loaded_at), MIN(loaded_at), DAY) AS days_open,
  CASE
    WHEN COUNT(DISTINCT pipeline_id) >= 5 THEN 'highly_recurring'
    WHEN COUNT(DISTINCT pipeline_id) >= 3 THEN 'recurring'
    WHEN COUNT(DISTINCT pipeline_id) = 2 THEN 'reappeared'
    ELSE 'single_observation'
  END AS recurrence_type
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_observations`
GROUP BY finding_id;