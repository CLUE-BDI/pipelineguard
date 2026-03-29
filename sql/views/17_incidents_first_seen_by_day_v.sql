CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents_first_seen_by_day_v` AS
SELECT
  DATE(MIN(loaded_at)) AS first_seen_date,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(severity) AS severity,
  incident_id,
  MAX(risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
GROUP BY incident_id;