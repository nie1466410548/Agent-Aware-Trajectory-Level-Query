SELECT 
  c.risk_group,
  p.profitability_tier,
  COUNT(*) AS n,
  ROUND(SUM(p.gross_profit), 2) AS total_gp
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group, p.profitability_tier
ORDER BY c.risk_group, p.profitability_tier