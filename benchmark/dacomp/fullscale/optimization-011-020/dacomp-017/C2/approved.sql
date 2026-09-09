-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c2" AS
SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL;

-- S59
SELECT "Customer ID", "yr", "Quantity" FROM temp."reuse_017_c2";

-- S62
SELECT "Customer ID", "yr", "Quantity" FROM temp."reuse_017_c2";

DROP TABLE temp."reuse_017_c2";
