-- Execute once before S37; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c4" AS
SELECT "Customer ID", gender, "Customer Segment" FROM customer_information GROUP BY "Customer ID";
