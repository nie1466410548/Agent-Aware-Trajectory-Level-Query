-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- S3
SELECT * FROM sheet1 LIMIT 20;

-- S4
SELECT COUNT(*) AS total_rows FROM sheet1;

-- S5
SELECT "Task Status", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Status";

-- S6
SELECT "Priority", COUNT(*) AS cnt FROM sheet1 GROUP BY "Priority";

-- S7
SELECT "Task Type", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Type";

-- S8
SELECT "Task Owner", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Owner" ORDER BY cnt DESC;

-- S9
SELECT * FROM sheet1 LIMIT 30;

-- S10
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status";

-- S11
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status";

-- S12
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed,
  SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
  SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS not_started,
  SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS paused
FROM sheet1;

-- S13
SELECT
  MIN("Planned Work Hours") AS min_planned, MAX("Planned Work Hours") AS max_planned,
  AVG("Planned Work Hours") AS avg_planned,
  SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) AS missing_actual_hours,
  SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) AS missing_quality,
  SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) AS missing_rework
FROM sheet1;

-- S14
SELECT MIN("Task Difficulty Coefficient") AS min_diff, MAX("Task Difficulty Coefficient") AS max_diff, AVG("Task Difficulty Coefficient") AS avg_diff
FROM sheet1;

-- S15
SELECT
  "Task Type",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff,
  AVG(CAST("Actual Work Hours" AS REAL)) AS avg_actual_hours,
  AVG("Planned Work Hours") AS avg_planned_hours,
  AVG(CAST("Actual Work Hours" AS REAL) * 1.0 / "Planned Work Hours") AS avg_hours_ratio,
  AVG(CAST("Rework Count" AS INTEGER)) AS avg_rework
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
  AND "Actual Work Hours" != '-'
  AND "Rework Count" != '-'
GROUP BY "Task Type"
ORDER BY "Task Type";

-- S16
SELECT
  "Priority",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
GROUP BY "Priority"
ORDER BY "Priority";

-- S17
SELECT
  "Task Owner",
  "Task Type",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks
FROM sheet1
GROUP BY "Task Owner", "Task Type"
ORDER BY "Task Owner", "Task Type";

-- S18
SELECT "Task ID", "Planned Deadline", "Actual Completion Time"
FROM sheet1
WHERE "Task Status" = 'Completed'
ORDER BY "Task ID"
LIMIT 30;

-- S19
SELECT
  MIN("Completion Quality Score") AS min_q,
  MAX("Completion Quality Score") AS max_q
FROM sheet1 WHERE "Completion Quality Score" != '-';

-- S20
SELECT MIN("Rework Count") AS min_r, MAX("Rework Count") AS max_r FROM sheet1 WHERE "Rework Count" != '-';

-- S21
SELECT
  CASE
    WHEN task_cnt <= 2 THEN '1-2'
    WHEN task_cnt <= 5 THEN '3-5'
    WHEN task_cnt <= 10 THEN '6-10'
    ELSE '11+'
  END AS owner_task_bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner", COUNT(*) AS task_cnt
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY owner_task_bucket
ORDER BY MIN(task_cnt);

-- S22
SELECT
  CASE
    WHEN task_cnt <= 2 THEN '1-2'
    WHEN task_cnt <= 5 THEN '3-5'
    WHEN task_cnt <= 10 THEN '6-10'
    ELSE '11+'
  END AS owner_task_bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner", SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS task_cnt
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY owner_task_bucket
ORDER BY MIN(task_cnt);

-- S23
SELECT
  "Task Owner",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
  SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS not_started,
  SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS paused
FROM sheet1
GROUP BY "Task Owner"
HAVING total_tasks >= 3
ORDER BY completed_tasks DESC
LIMIT 30;

-- S24
SELECT
  CASE
    WHEN completed = 0 THEN '0 completed'
    WHEN completed = 1 THEN '1 completed'
    WHEN completed BETWEEN 2 AND 4 THEN '2-4 completed'
    ELSE '5+ completed'
  END AS bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner",
    SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed,
    COUNT(*) AS total
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY bucket
ORDER BY MIN(completed);

-- S25
SELECT "Task Type", COUNT(DISTINCT "Task Owner") AS owner_count
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type";

-- S26
SELECT COUNT(*) AS multi_type_owners FROM (
  SELECT "Task Owner" FROM sheet1 GROUP BY "Task Owner" HAVING COUNT(DISTINCT "Task Type") > 1
);

-- S27
SELECT
  "Task Type",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Actual Work Hours" AS REAL) END),1) AS avg_actual,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Completion Quality Score" AS REAL) END),2) AS avg_quality
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type";

-- S28
SELECT
  "Task Status",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned
FROM sheet1
GROUP BY "Task Status"
ORDER BY "Task Status";

-- S29
SELECT "Priority", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Priority", "Task Status"
ORDER BY "Priority", "Task Status";

-- S30
WITH t AS (
  SELECT
    "Task Owner",
    "Task Type",
    "Task Status",
    "Priority",
    "Task Difficulty Coefficient",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3
         WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END AS pw,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
         THEN julianday("Actual Completion Time") - julianday("Planned Deadline") END AS late_days,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  ROUND(1.0 * SUM(completed) / COUNT(*), 4) AS completion_rate,
  ROUND(1.0 * SUM(on_time) / NULLIF(SUM(completed),0), 4) AS on_time_rate,
  ROUND(AVG(quality), 4) AS avg_quality,
  ROUND(1.0 * SUM(pw * completed) / NULLIF(SUM(pw), 0), 4) AS priority_weighted_completion,
  ROUND(AVG(eff), 4) AS hours_efficiency,
  ROUND(AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework / 3.0 END), 4) AS rework_avoidance,
  ROUND(AVG(late_days), 3) AS avg_late_days,
  ROUND(AVG("Task Difficulty Coefficient"), 3) AS avg_diff
FROM t
GROUP BY "Task Owner"
ORDER BY "Task Owner";

-- S31
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  ROUND(AVG(completion_rate),3) AS avg_completion_rate,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN on_time_rate END),3) AS avg_on_time,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN avg_quality END),3) AS avg_quality,
  ROUND(AVG(priority_weighted_completion),3) AS avg_prio_completion,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN hours_efficiency END),3) AS avg_eff,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN rework_avoidance END),3) AS avg_rework_avoid
FROM (
  SELECT "Task Owner", COUNT(*) AS total_tasks,
    SUM(completed) AS completed_tasks,
    1.0*SUM(completed)/COUNT(*) AS completion_rate,
    1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
    AVG(quality) AS avg_quality,
    1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
      /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
    AVG(eff) AS hours_efficiency,
    AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance
  FROM t
  GROUP BY "Task Owner"
);

-- S32
SELECT
  "Task Type",
  ROUND(AVG(1.0*completed/total),3) AS avg_completion_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN on_time/completed END),3) AS avg_on_time_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN quality_sum/completed END),3) AS avg_quality
FROM (
  SELECT "Task Owner", "Task Type", COUNT(*) AS total,
    SUM(CASE WHEN "Task Status"='Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN "Task Status"='Completed' AND "Actual Completion Time" != '-' AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline") THEN 1 ELSE 0 END) AS on_time,
    SUM(CASE WHEN "Task Status"='Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) ELSE 0 END) AS quality_sum
  FROM sheet1
  GROUP BY "Task Owner", "Task Type"
)
GROUP BY "Task Type"
ORDER BY "Task Type";

-- BUILD C2 before S33
CREATE TEMP TABLE "reuse_013_c2" AS
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND on_time=1 THEN 1 ELSE 0 END) AS hp_on_time,
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM t
GROUP BY "Task Owner";

-- S33
SELECT "Task Owner", "task_type", "total_tasks", "completed_tasks", "completion_rate", "on_time_rate", "quality_norm", "priority_weighted_completion", "hours_efficiency", "rework_avoidance", "hp_total", "hp_completed", "hp_on_time", "avg_diff" FROM temp."reuse_013_c2";

-- S34
SELECT "Task Owner", "task_type", "total_tasks", "completed_tasks", "completion_rate", "on_time_rate", "quality_norm", "priority_weighted_completion", "hours_efficiency", "rework_avoidance", "hp_total", "hp_completed", "hp_on_time", "avg_diff" FROM temp."reuse_013_c2";

-- S35
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS is_comp
  FROM sheet1
)
SELECT
  "Task Owner", MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-' THEN 1 ELSE 0 END) AS timed_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-' THEN 1 ELSE 0 END) AS scored_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) AS eff_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-' THEN 1 ELSE 0 END) AS rework_completed,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance
FROM t
GROUP BY "Task Owner";

-- S36
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework
  FROM sheet1
)
SELECT
  "Task Owner", MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-' THEN 1 ELSE 0 END) AS timed_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-' THEN 1 ELSE 0 END) AS scored_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) AS eff_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-' THEN 1 ELSE 0 END) AS rework_completed,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed
FROM t
GROUP BY "Task Owner";

-- S37
SELECT "Task Owner", ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM sheet1 GROUP BY "Task Owner";

DROP TABLE temp."reuse_013_c2";
COMMIT;
