SELECT
  __g3 AS "Diet quality",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g3;
