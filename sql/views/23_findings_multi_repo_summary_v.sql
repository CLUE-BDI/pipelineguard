CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.findings_multi_repo_summary_v` AS
SELECT
  repo,
  tool,
  category,
  severity,
  DATE(timestamp) AS finding_date,
  COUNT(*) AS finding_count
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.findings_normalized`
GROUP BY repo, tool, category, severity, finding_date;