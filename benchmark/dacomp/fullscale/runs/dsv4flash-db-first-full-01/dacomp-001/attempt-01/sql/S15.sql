-- Sales per enterprise per year to assess stability
SELECT ci."Enterprise Code", ci."Credit Rating",
       strftime('%Y', s."Invoice Date") AS year,
       SUM(s."Amount Including Tax") AS yearly_revenue
FROM ch___company_info ci
JOIN ch___sales_invoices s ON ci."Enterprise Code" = s."Enterprise Code" AND s."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code", year
ORDER BY ci."Enterprise Code", year