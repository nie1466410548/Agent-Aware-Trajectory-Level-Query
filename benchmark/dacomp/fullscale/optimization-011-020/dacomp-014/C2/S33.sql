SELECT
  ROUND(1.0 * SUM(__a30) / SUM(__a0) * 100, 1) AS "pct_viral_5m",
  ROUND(1.0 * SUM(__a31) / SUM(__a0) * 100, 1) AS "pct_viral_2m"
FROM temp."reuse_014_c2";
