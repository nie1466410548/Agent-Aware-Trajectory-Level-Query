-- Input costs (valid invoices) per enterprise
SELECT ci."Enterprise Code",
       COALESCE(SUM(i."Amount Including Tax"), 0) AS total_input
FROM ch___company_info ci
LEFT JOIN ch___input_invoices i ON ci."Enterprise Code" = i."Enterprise Code" AND i."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code"
ORDER BY ci."Enterprise Code"