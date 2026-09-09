-- Execute once before S34; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c3" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";
