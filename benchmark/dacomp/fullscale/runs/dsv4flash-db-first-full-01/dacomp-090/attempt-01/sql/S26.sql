SELECT 
  CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
  activity_status,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END), 2) AS pct
FROM quickbooks__customer_analytics
GROUP BY risk_group, activity_status
ORDER BY risk_group, n DESC