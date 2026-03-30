CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents_multi_repo_summary_v` AS
SELECT
  repo,
  severity,
  DATE(timestamp) AS incident_date,
  COUNT(*) AS incident_count,
  AVG(risk_score) AS avg_risk_score,
  MAX(risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents`
GROUP BY repo, severity, incident_date;