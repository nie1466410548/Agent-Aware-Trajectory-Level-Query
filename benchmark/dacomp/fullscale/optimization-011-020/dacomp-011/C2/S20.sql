SELECT
  __g6 AS "mh_cat",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study"
FROM temp."reuse_011_c2"
GROUP BY
  __g6
ORDER BY
  avg_exam DESC;
