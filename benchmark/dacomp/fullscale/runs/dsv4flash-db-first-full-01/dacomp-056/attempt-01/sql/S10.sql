SELECT customer_tier, COUNT(DISTINCT marketo_lead_id) AS n, 
       AVG(portfolio_contribution_pct) AS avg_portfolio_contrib,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
GROUP BY customer_tier
ORDER BY CASE customer_tier 
  WHEN 'Platinum' THEN 1 WHEN 'Gold' THEN 2 
  WHEN 'Silver' THEN 3 WHEN 'Bronze' THEN 4 WHEN 'Basic' THEN 5 END