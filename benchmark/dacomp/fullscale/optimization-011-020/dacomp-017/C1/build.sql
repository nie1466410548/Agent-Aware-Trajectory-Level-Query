-- Execute once before S50; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c1" AS
SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL;
