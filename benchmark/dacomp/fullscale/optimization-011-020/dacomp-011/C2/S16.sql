SELECT
  __g3 AS "val",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g3
ORDER BY
  avg_exam DESC;
