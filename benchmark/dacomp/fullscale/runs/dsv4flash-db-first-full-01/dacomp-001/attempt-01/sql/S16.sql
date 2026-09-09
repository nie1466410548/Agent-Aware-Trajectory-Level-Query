-- Downstream dependency: share of top-1 buyer in total sales (valid invoices)
WITH cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s
  WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
tot AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total
  FROM ch___sales_invoices
  WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
)
SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share, COUNT(c.partner) AS n_customers
FROM cust c JOIN tot t ON c.code = t.code
GROUP BY c.code
ORDER BY top1_buyer_share DESC