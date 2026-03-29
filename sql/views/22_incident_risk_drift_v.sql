CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_risk_drift_v` AS
WITH ranked AS (
  SELECT
    incident_id,
    repo,
    pipeline_id,
    loaded_at,
    risk_score,
    ROW_NUMBER() OVER (PARTITION BY incident_id ORDER BY loaded_at ASC) AS first_rank,
    ROW_NUMBER() OVER (PARTITION BY incident_id ORDER BY loaded_at DESC) AS last_rank
  FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
),
first_scores AS (
  SELECT
    incident_id,
    risk_score AS first_risk_score
  FROM ranked
  WHERE first_rank = 1
),
last_scores AS (
  SELECT
    incident_id,
    risk_score AS last_risk_score
  FROM ranked
  WHERE last_rank = 1
)
SELECT
  r.incident_id,
  r.repo,
  f.first_risk_score,
  l.last_risk_score,
  l.last_risk_score - f.first_risk_score AS risk_score_change
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_recurrence_v` r
JOIN first_scores f USING (incident_id)
JOIN last_scores l USING (incident_id);