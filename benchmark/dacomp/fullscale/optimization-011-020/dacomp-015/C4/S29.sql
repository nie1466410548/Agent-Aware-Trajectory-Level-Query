SELECT
  __g6 AS "Date Published",
  SUM(__a0) AS "cnt",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_watch",
  (
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ) AS "avg_show"
FROM temp."reuse_015_c4"
GROUP BY
  __g6
ORDER BY
  cnt DESC;
