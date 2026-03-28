CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents_by_repo_day_v` AS
SELECT
  DATE(timestamp) AS incident_date,
  repo,
  severity,
  COUNT(*) AS incident_count,
  AVG(risk_score) AS avg_risk_score,
  MAX(risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents`
GROUP BY 1, 2, 3;