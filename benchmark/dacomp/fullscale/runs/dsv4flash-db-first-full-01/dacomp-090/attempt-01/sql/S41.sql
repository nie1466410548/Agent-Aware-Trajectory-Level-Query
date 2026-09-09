SELECT 
  c.risk_group,
  COUNT(DISTINCT p.customer_id) AS n_customers,
  ROUND(SUM(p.gross_profit),2) AS sum_gross_profit,
  ROUND(SUM(p.risk_adjusted_profit),2) AS sum_risk_adj_profit
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group