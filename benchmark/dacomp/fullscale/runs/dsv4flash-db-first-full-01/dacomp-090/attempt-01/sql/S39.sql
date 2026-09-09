
  SELECT 
    CASE WHEN c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
    p.profitability_tier,
    COUNT(*) AS n_invoices,
    ROUND(SUM(p.gross_profit),2) AS total_gp
  FROM quickbooks__profitability_analysis p
  INNER JOIN quickbooks__customer_analytics c ON p.customer_id = c.customer_id
  GROUP BY risk_group, p.profitability_tier
  ORDER BY risk_group, p.profitability_tier
