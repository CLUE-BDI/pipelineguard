CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.findings_first_seen_by_day_v` AS
SELECT
  DATE(MIN(loaded_at)) AS first_seen_date,
  ANY_VALUE(repo) AS repo,
  ANY_VALUE(category) AS category,
  ANY_VALUE(severity) AS severity,
  ANY_VALUE(tool) AS tool,
  finding_id
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.finding_observations`
GROUP BY finding_id;