CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.repo_risk_v` AS
SELECT
  repo,
  COUNT(*) AS incident_count,
  AVG(risk_score) AS avg_risk_score,
  MAX(risk_score) AS max_risk_score,
  SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_incidents,
  SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) AS high_incidents
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incidents`
GROUP BY repo;