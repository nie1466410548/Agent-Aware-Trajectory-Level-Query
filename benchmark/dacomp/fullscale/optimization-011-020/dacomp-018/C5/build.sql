-- Execute once before S37; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c5" AS
SELECT "Customer ID", SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";
