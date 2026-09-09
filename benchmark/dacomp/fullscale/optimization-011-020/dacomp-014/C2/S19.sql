SELECT
  __g5 AS "rank_band",
  __g1 AS "Main Category",
  SUM(__a0) AS "count"
FROM temp."reuse_014_c2"
GROUP BY
  __g5,
  __g1
ORDER BY
  rank_band,
  count DESC;
