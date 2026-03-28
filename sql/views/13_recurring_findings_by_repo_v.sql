CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.recurring_findings_by_repo_v` AS
SELECT
  repo,
  COUNTIF(pipeline_count > 1) AS recurring_finding_count,
  COUNT(*) AS total_unique_findings,
  AVG(pipeline_count) AS avg_pipeline_count,
  AVG(days_open) AS avg_days_open
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_recurrence_v`
GROUP BY repo;