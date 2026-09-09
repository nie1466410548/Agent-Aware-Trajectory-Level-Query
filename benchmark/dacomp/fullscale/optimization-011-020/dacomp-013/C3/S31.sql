WITH t AS (
  SELECT
    *
  FROM temp."reuse_013_c3"
)
SELECT
  ROUND(AVG(completion_rate), 3) AS "avg_completion_rate",
  ROUND(AVG(CASE WHEN completed_tasks > 0 THEN on_time_rate END), 3) AS "avg_on_time",
  ROUND(AVG(CASE WHEN completed_tasks > 0 THEN avg_quality END), 3) AS "avg_quality",
  ROUND(AVG(priority_weighted_completion), 3) AS "avg_prio_completion",
  ROUND(AVG(CASE WHEN completed_tasks > 0 THEN hours_efficiency END), 3) AS "avg_eff",
  ROUND(AVG(CASE WHEN completed_tasks > 0 THEN rework_avoidance END), 3) AS "avg_rework_avoid"
FROM (
  SELECT
    "Task Owner",
    COUNT(*) AS total_tasks,
    SUM(completed) AS completed_tasks,
    1.0 * SUM(completed) / COUNT(*) AS completion_rate,
    1.0 * SUM(on_time) / NULLIF(SUM(completed), 0) AS on_time_rate,
    AVG(quality) AS avg_quality,
    1.0 * SUM(
      CASE
        WHEN "Priority" = 'Urgent'
        THEN 4
        WHEN "Priority" = 'High'
        THEN 3
        WHEN "Priority" = 'Medium'
        THEN 2
        WHEN "Priority" = 'Low'
        THEN 1
      END * completed
    ) / NULLIF(
      SUM(
        CASE
          WHEN "Priority" = 'Urgent'
          THEN 4
          WHEN "Priority" = 'High'
          THEN 3
          WHEN "Priority" = 'Medium'
          THEN 2
          WHEN "Priority" = 'Low'
          THEN 1
        END
      ),
      0
    ) AS priority_weighted_completion,
    AVG(eff) AS hours_efficiency,
    AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) AS rework_avoidance
  FROM t
  GROUP BY
    "Task Owner"
);
