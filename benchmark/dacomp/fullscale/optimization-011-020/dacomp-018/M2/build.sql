-- Execute once before S20; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_m2" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";
CREATE INDEX temp."reuse_018_m2_customer" ON "reuse_018_m2"("Customer ID");
