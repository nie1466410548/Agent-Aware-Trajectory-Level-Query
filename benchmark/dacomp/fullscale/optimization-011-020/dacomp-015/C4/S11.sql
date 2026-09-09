SELECT
  __g2 AS "Decoration",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g2
ORDER BY
  cnt DESC;
