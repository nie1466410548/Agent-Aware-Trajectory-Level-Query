SELECT
  __g0 AS "parent_edu",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND(MIN(__a2), 2) AS "min_exam",
  ROUND(MAX(__a3), 2) AS "max_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0
ORDER BY
  avg_exam DESC;
