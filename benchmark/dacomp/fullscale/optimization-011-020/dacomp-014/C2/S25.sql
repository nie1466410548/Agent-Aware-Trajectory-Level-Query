SELECT
  __g6 AS "id_prefix",
  SUM(__a0) AS "cnt"
FROM temp."reuse_014_c2"
GROUP BY
  __g6
ORDER BY
  cnt DESC;
