-- Comprehensive metrics per company
WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
),
cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
cust_conc AS (
  SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share
  FROM cust c JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON c.code = t.code
  GROUP BY c.code
),
supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
supp_conc AS (
  SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share
  FROM supp s JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON s.code = t.code
  GROUP BY s.code
)
SELECT ci."Enterprise Code" AS code, ci."Company Name", ci."Credit Rating", ci."Defaulted",
       COALESCE(rev.total_revenue, 0) AS total_revenue,
       COALESCE(inp.total_input, 0) AS total_input,
       COALESCE(rev.total_revenue, 0) - COALESCE(inp.total_input, 0) AS profit,
       CASE WHEN COALESCE(rev.total_revenue, 0) > 0 
            THEN (COALESCE(rev.total_revenue, 0) - COALESCE(inp.total_input, 0)) / COALESCE(rev.total_revenue, 0) 
            ELSE 0 END AS profit_margin,
       COALESCE(cust_conc.top1_buyer_share, 0) AS top1_buyer_share,
       COALESCE(supp_conc.top1_supplier_share, 0) AS top1_supplier_share
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
LEFT JOIN cust_conc ON ci."Enterprise Code" = cust_conc.code
LEFT JOIN supp_conc ON ci."Enterprise Code" = supp_conc.code
ORDER BY ci."Credit Rating", ci."Enterprise Code"