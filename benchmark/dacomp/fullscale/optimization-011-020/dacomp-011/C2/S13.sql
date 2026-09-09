SELECT
  __g0 AS "parent_edu",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    SUM(__a10) - SUM(__a11) * SUM(__a11) / SUM(__a0)
  ) / (
    SUM(__a0) - 1
  ), 2) AS "var_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0
ORDER BY
  parent_edu;
