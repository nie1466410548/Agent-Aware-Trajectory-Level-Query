-- Revenue capacity: total sales amount (valid invoices) per enterprise
SELECT ci."Enterprise Code", ci."Company Name", ci."Credit Rating", ci."Defaulted",
       COALESCE(SUM(s."Amount Including Tax"), 0) AS total_revenue
FROM ch___company_info ci
LEFT JOIN ch___sales_invoices s ON ci."Enterprise Code" = s."Enterprise Code" AND s."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code"
ORDER BY ci."Credit Rating", total_revenue DESC