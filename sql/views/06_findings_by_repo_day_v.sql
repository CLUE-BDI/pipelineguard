CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.findings_by_repo_day_v` AS
SELECT
  DATE(timestamp) AS finding_date,
  repo,
  severity,
  category,
  tool,
  COUNT(*) AS finding_count
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.findings_normalized`
GROUP BY 1, 2, 3, 4, 5;