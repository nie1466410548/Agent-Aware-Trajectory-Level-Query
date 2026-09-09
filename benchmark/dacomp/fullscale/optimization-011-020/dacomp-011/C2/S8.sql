SELECT
  __g0 AS "parent_edu",
  __g1 AS "Gender",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  SUM(__a0) AS "n"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g1
ORDER BY
  parent_edu,
  __g1;
