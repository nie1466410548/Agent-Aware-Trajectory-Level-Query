SELECT p.customer_id, c.customer_name,
  ROUND(SUM(p.gross_profit),2) AS gp, ROUND(SUM(p.invoice_total),2) AS inv_total,
  COUNT(*) AS n_inv
FROM quickbooks__profitability_analysis p
INNER JOIN quickbooks__customer_analytics c ON p.customer_id = c.customer_id
WHERE c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000
GROUP BY p.customer_id
ORDER BY gp ASC
LIMIT 20