SELECT 
  c.risk_group,
  p.profitability_tier,
  COUNT(*) AS n_invoices,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY c.risk_group), 2) AS pct_invoices,
  ROUND(SUM(p.gross_profit),2) AS total_gp,
  ROUND(AVG(p.invoice_gross_margin_pct),2) AS avg_margin_pct
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group, p.profitability_tier
ORDER BY c.risk_group, n_invoices DESC