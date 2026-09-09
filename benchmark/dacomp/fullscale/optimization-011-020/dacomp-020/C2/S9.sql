SELECT
  __g1 AS "Gender",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g1;
