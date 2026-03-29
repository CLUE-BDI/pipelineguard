CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_recurrence_by_severity_v` AS
SELECT
  severity,
  recurrence_type,
  COUNT(*) AS incident_count,
  AVG(avg_risk_score) AS avg_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_recurrence_v`
GROUP BY severity, recurrence_type;