SELECT
  __g6 AS "Extracurricular activity participation",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g6;
