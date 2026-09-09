SELECT
  __g3 AS "vstatus",
  SUM(__a0) AS "cnt",
  ROUND(100.0 * SUM(__a31) / SUM(__a0), 1) AS "pct_viral_2m",
  ROUND(100.0 * SUM(__a32) / SUM(__a0), 1) AS "pct_viral_1m",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank"
FROM temp."reuse_014_c2"
GROUP BY
  __g3;
