SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn,
       AVG(account_age_days) AS avg_age,
       AVG(days_since_last_activity) AS avg_days_inactive
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier IN ('Gold', 'Platinum')
  AND portfolio_contribution_pct > 0.05
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC