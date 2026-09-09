SELECT ROUND(SUM(gross_profit), 2) AS total_gross_profit_all,
  ROUND(SUM(invoice_total), 2) AS total_invoice_all
FROM quickbooks__profitability_analysis