-- Execute once before S19; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c1" AS
SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID";
