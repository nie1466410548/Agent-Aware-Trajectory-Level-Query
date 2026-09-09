SELECT
  __g9 AS "parent_edu",
  __g2 AS "diet",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g9,
  __g2
ORDER BY
  parent_edu,
  diet;
