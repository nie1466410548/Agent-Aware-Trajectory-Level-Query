SELECT
  __g4 AS "Parents' education level",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g4;
