-- Aggregate metrics by rating
WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
)
SELECT ci."Credit Rating",
       COUNT(*) AS n_firms,
       SUM(CASE WHEN ci."Defaulted" = 'Yes' THEN 1 ELSE 0 END) AS n_defaults,
       ROUND(AVG(rev.total_revenue), 0) AS avg_revenue,
       ROUND(AVG(CASE WHEN rev.total_revenue > 0 THEN (rev.total_revenue - COALESCE(inp.total_input, 0))/rev.total_revenue ELSE NULL END), 4) AS avg_margin,
       ROUND(MIN(rev.total_revenue), 0) AS min_revenue,
       ROUND(MAX(rev.total_revenue), 0) AS max_revenue
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
GROUP BY ci."Credit Rating"
ORDER BY ci."Credit Rating"