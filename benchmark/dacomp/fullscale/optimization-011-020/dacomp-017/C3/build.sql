-- Execute once before S5; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c3" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product Category" AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2, SUM(CASE WHEN "Discount" = 'xxx' OR "Quantity" = 'abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) AS __a5, MAX("Order Date") AS __a6, MIN("Order Date") AS __a7 FROM "order_information"  GROUP BY SUBSTRING("Order Date", 1, 4), "Product Category";
