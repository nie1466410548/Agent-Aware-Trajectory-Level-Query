-- Execute once before S37; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c9" AS
SELECT "Quantity" AS __g0, SUBSTRING("Order Date", 1, 4) AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2 FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas' GROUP BY "Quantity", SUBSTRING("Order Date", 1, 4);
