SELECT invoice_id, customer_id, transaction_date, revenue_month_start, customer_margin_volatility, invoice_total, gross_profit
FROM quickbooks__profitability_analysis
WHERE customer_id = 'CUS00031796345'
ORDER BY transaction_date