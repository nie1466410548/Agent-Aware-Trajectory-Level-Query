-- Execute once before S65; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c15" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product" AS __g1, SUM(CAST("Discount" AS REAL)) AS __a0_sum, COUNT(CAST("Discount" AS REAL)) AS __a0_n, SUM(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_sum, COUNT(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_n FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Discount" <> 'xxx' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL GROUP BY SUBSTRING("Order Date", 1, 4), "Product";
