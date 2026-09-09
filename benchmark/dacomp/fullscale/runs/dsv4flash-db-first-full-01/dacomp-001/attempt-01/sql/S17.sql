-- Upstream dependency: share of top-1 supplier in total inputs (valid invoices)
WITH supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i
  WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
tot AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total
  FROM ch___input_invoices
  WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
)
SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share, COUNT(s.partner) AS n_suppliers
FROM supp s JOIN tot t ON s.code = t.code
GROUP BY s.code
ORDER BY top1_supplier_share DESC