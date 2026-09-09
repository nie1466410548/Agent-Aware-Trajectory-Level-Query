-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c7" AS
SELECT "Customer ID" AS __g0, COUNT(*) AS __a0 FROM "customer_information"  GROUP BY "Customer ID";

-- S5
SELECT
  SUM(__a0) AS "total_customers"
FROM temp."reuse_018_c7";

-- S13
SELECT
  SUM(__a0) AS "COUNT(*)"
FROM temp."reuse_018_c7";

-- S15
SELECT
  __g0 AS "Customer ID",
  SUM(__a0) AS "cnt"
FROM temp."reuse_018_c7"
GROUP BY
  __g0
ORDER BY
  cnt DESC
LIMIT 10;

DROP TABLE temp."reuse_018_c7";
