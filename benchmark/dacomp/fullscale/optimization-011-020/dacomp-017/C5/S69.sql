-- NOT APPROVED: result comparison failed. Use the original SQL for this query.
SELECT
  __g6 AS "Customer ID",
  SUM(__a2) AS "profit",
  SUM(__a3) AS "sales"
FROM temp."reuse_017_c5"
GROUP BY
  __g6;
