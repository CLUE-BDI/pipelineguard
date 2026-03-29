CREATE OR REPLACE VIEW `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_lifecycle_v` AS
WITH first_obs AS (
  SELECT
    incident_id,
    ARRAY_AGG(
      STRUCT(
        pipeline_id,
        commit_sha,
        branch,
        loaded_at,
        severity,
        risk_score
      )
      ORDER BY loaded_at ASC
      LIMIT 1
    )[OFFSET(0)] AS first_observation
  FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
  GROUP BY incident_id
),
last_obs AS (
  SELECT
    incident_id,
    ARRAY_AGG(
      STRUCT(
        pipeline_id,
        commit_sha,
        branch,
        loaded_at,
        severity,
        risk_score
      )
      ORDER BY loaded_at DESC
      LIMIT 1
    )[OFFSET(0)] AS last_observation
  FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_observations`
  GROUP BY incident_id
)
SELECT
  r.incident_id,
  r.repo,
  r.severity,
  r.observation_count,
  r.pipeline_count,
  r.commit_count,
  r.days_open,
  r.avg_risk_score,
  r.max_risk_score,
  r.recurrence_type,
  first_observation.pipeline_id AS first_seen_pipeline_id,
  first_observation.commit_sha AS first_seen_commit_sha,
  first_observation.branch AS first_seen_branch,
  first_observation.loaded_at AS first_seen_at,
  first_observation.severity AS first_seen_severity,
  first_observation.risk_score AS first_seen_risk_score,
  last_observation.pipeline_id AS last_seen_pipeline_id,
  last_observation.commit_sha AS last_seen_commit_sha,
  last_observation.branch AS last_seen_branch,
  last_observation.loaded_at AS last_seen_at,
  last_observation.severity AS last_seen_severity,
  last_observation.risk_score AS last_seen_risk_score
FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.incident_recurrence_v` r
JOIN first_obs USING (incident_id)
JOIN last_obs USING (incident_id);