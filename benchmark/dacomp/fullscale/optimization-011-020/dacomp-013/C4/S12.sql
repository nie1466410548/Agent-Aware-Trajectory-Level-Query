SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "completed",
  SUM(__a2) AS "in_progress",
  SUM(__a3) AS "not_started",
  SUM(__a4) AS "paused"
FROM temp."reuse_013_c4";
