CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_first_last_seen_v` AS
SELECT
  incident_id,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(severity) AS severity,
  MIN(loaded_at) AS first_seen_at,
  MAX(loaded_at) AS last_seen_at,
  DATE(MIN(loaded_at)) AS first_seen_date,
  DATE(MAX(loaded_at)) AS last_seen_date,
  COUNT(*) AS observation_count,
  COUNT(DISTINCT pipeline_id) AS pipeline_count,
  COUNT(DISTINCT commit_sha) AS commit_count,
  AVG(risk_score) AS avg_risk_score,
  MAX(risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
GROUP BY incident_id;