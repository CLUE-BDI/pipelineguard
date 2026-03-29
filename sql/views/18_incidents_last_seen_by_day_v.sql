CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents_last_seen_by_day_v` AS
SELECT
  DATE(MAX(loaded_at)) AS last_seen_date,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(severity) AS severity,
  incident_id,
  MAX(risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
GROUP BY incident_id;