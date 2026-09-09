SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier NOT IN ('Gold', 'Platinum')
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC