SELECT
  __g2 AS "Clarity",
  SUM(__a0) AS "n"
FROM temp."reuse_012_c3"
GROUP BY
  __g2
ORDER BY
  __g2;
