SELECT
  __g2 AS "Inventory Discrepancy Rate",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c3"
GROUP BY
  __g2
ORDER BY
  cnt DESC
LIMIT 15;
