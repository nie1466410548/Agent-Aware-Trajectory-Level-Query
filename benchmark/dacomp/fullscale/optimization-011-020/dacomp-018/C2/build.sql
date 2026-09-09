-- Execute once before S20; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c2" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";
