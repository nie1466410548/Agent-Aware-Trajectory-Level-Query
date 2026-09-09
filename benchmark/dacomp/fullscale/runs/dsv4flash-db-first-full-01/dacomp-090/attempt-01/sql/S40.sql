
  SELECT 
    CASE 
      WHEN risk_score < 40 THEN 'Low (30-40)'
      WHEN risk_score < 50 THEN 'Medium (40-50)'
      WHEN risk_score < 60 THEN 'High (50-60)'
      ELSE 'Critical (60+)'
    END AS risk_tier,
    COUNT(*) AS n_customers,
    ROUND(SUM(outstanding_balance),2) AS total_outstanding,
    ROUND(AVG(risk_score),2) AS avg_risk_score
  FROM (
    SELECT customer_id, outstanding_balance,
      (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
    FROM quickbooks__customer_analytics
    WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
  )
  GROUP BY risk_tier
  ORDER BY MIN(risk_score)
