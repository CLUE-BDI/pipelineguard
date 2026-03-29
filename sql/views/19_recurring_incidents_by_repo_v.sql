CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.recurring_incidents_by_repo_v` AS
SELECT
  repo,
  COUNTIF(pipeline_count > 1) AS recurring_incident_count,
  COUNT(*) AS total_unique_incidents,
  AVG(pipeline_count) AS avg_pipeline_count,
  AVG(days_open) AS avg_days_open,
  AVG(avg_risk_score) AS avg_risk_score,
  MAX(max_risk_score) AS max_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_recurrence_v`
GROUP BY repo;