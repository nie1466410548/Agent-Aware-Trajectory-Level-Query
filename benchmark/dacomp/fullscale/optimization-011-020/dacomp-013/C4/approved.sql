-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_013_c4" AS
SELECT "Task Status" AS __g0, "Priority" AS __g1, "Task Type" AS __g2, "Task Owner" AS __g3, COUNT(*) AS __a0, SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS __a4, MIN("Planned Work Hours") AS __a5, MAX("Planned Work Hours") AS __a6, SUM("Planned Work Hours") AS __a7_sum, COUNT("Planned Work Hours") AS __a7_n, SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) AS __a10, MIN("Task Difficulty Coefficient") AS __a11, MAX("Task Difficulty Coefficient") AS __a12, SUM("Task Difficulty Coefficient") AS __a13_sum, COUNT("Task Difficulty Coefficient") AS __a13_n, SUM(CASE WHEN "Task Status" = 'Completed' THEN CAST("Actual Work Hours" AS REAL) END) AS __a14_sum, COUNT(CASE WHEN "Task Status" = 'Completed' THEN CAST("Actual Work Hours" AS REAL) END) AS __a14_n, SUM(CASE WHEN "Task Status" = 'Completed' THEN CAST("Completion Quality Score" AS REAL) END) AS __a15_sum, COUNT(CASE WHEN "Task Status" = 'Completed' THEN CAST("Completion Quality Score" AS REAL) END) AS __a15_n FROM "sheet1"  GROUP BY "Task Status", "Priority", "Task Type", "Task Owner";

-- S4
SELECT
  SUM(__a0) AS "total_rows"
FROM temp."reuse_013_c4";

-- S5
SELECT
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g0;

-- S6
SELECT
  __g1 AS "Priority",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g1;

-- S7
SELECT
  __g2 AS "Task Type",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g2;

-- S8
SELECT
  __g3 AS "Task Owner",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g3
ORDER BY
  cnt DESC;

-- S10
SELECT
  __g2 AS "Task Type",
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g2,
  __g0
ORDER BY
  __g2,
  __g0;

-- S11
SELECT
  __g2 AS "Task Type",
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g2,
  __g0
ORDER BY
  __g2,
  __g0;

-- S12
SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "completed",
  SUM(__a2) AS "in_progress",
  SUM(__a3) AS "not_started",
  SUM(__a4) AS "paused"
FROM temp."reuse_013_c4";

-- S13
SELECT
  MIN(__a5) AS "min_planned",
  MAX(__a6) AS "max_planned",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_planned",
  SUM(__a8) AS "missing_actual_hours",
  SUM(__a9) AS "missing_quality",
  SUM(__a10) AS "missing_rework"
FROM temp."reuse_013_c4";

-- S17
SELECT
  __g3 AS "Task Owner",
  __g2 AS "Task Type",
  SUM(__a0) AS "total_tasks",
  SUM(__a1) AS "completed_tasks"
FROM temp."reuse_013_c4"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  __g2;

-- S27
SELECT
  __g2 AS "Task Type",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 1) AS "avg_planned",
  ROUND((
    1.0 * SUM(__a14_sum) / NULLIF(SUM(__a14_n), 0)
  ), 1) AS "avg_actual",
  ROUND((
    1.0 * SUM(__a15_sum) / NULLIF(SUM(__a15_n), 0)
  ), 2) AS "avg_quality"
FROM temp."reuse_013_c4"
GROUP BY
  __g2
ORDER BY
  __g2;

-- S28
SELECT
  __g0 AS "Task Status",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 1) AS "avg_planned"
FROM temp."reuse_013_c4"
GROUP BY
  __g0
ORDER BY
  __g0;

-- S29
SELECT
  __g1 AS "Priority",
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  __g0;

-- S37
SELECT
  __g3 AS "Task Owner",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff"
FROM temp."reuse_013_c4"
GROUP BY
  __g3;

DROP TABLE temp."reuse_013_c4";
