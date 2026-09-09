SELECT COUNT(DISTINCT p.customer_id) AS customers_in_profit, COUNT(*) AS invoice_count,
  ROUND(SUM(p.gross_profit), 2) AS total_gross_profit_high_risk,
  ROUND(SUM(p.invoice_total), 2) AS total_invoice_high_risk
FROM quickbooks__profitability_analysis p
INNER JOIN (
  SELECT customer_id FROM quickbooks__customer_analytics 
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
) c ON p.customer_id = c.customer_id