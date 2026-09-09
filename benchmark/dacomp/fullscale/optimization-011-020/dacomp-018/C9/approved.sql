-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c9" AS
SELECT * FROM "product_browsing" WHERE "Product Category" = 'Fashion';

-- S9
SELECT * FROM temp."reuse_018_c9" AS product_browsing WHERE "Product Category" = 'Fashion' LIMIT 5;

-- S30
SELECT
  COUNT(*) AS "rows_cnt",
  COUNT(DISTINCT "Customer ID") AS "customers"
FROM temp."reuse_018_c9" AS product_browsing
WHERE
  "Product Category" = 'Fashion';

DROP TABLE temp."reuse_018_c9";
