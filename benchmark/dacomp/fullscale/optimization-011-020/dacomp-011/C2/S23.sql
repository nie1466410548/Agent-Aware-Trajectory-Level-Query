SELECT
  __g0 AS "parent_edu",
  __g8 AS "pt_job",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g8
ORDER BY
  parent_edu,
  pt_job;
