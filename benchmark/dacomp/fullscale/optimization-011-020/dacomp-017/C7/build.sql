-- Execute once before S32; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c7" AS
SELECT "Quantity" AS __g0, "Discount" AS __g1, SUBSTRING("Order Date", 1, 4) AS __g2, COUNT(*) AS __a0, SUM(sales) AS __a1, SUM(profit) AS __a2 FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds' GROUP BY "Quantity", "Discount", SUBSTRING("Order Date", 1, 4);
