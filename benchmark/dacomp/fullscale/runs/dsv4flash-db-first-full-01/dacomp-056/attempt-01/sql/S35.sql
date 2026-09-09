WITH dedup AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY marketo_lead_id ORDER BY rfm_avg_score DESC, rfm_score DESC) AS rn
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
),
groups AS (
  SELECT *,
    CASE WHEN customer_tier IN ('Gold','Platinum') AND portfolio_contribution_pct > 0.05 THEN 'HVE'
         ELSE 'SMB' END AS customer_group
  FROM dedup WHERE rn = 1
)
SELECT customer_group, COUNT(*) AS n,
  AVG(recency_score) AS avg_recency,
  AVG(frequency_score) AS avg_frequency,
  AVG(monetary_score) AS avg_monetary,
  AVG(rfm_avg_score) AS avg_rfm,
  AVG(estimated_customer_ltv) AS avg_ltv,
  AVG(customer_health_score) AS avg_health,
  AVG(churn_probability) AS avg_churn,
  AVG(account_age_days) AS avg_age,
  AVG(days_since_last_activity) AS avg_days_inactive,
  AVG(portfolio_contribution_pct) AS avg_portfolio,
  AVG(investment_priority_score) AS avg_priority,
  AVG(expected_annual_revenue) AS avg_annual_rev
FROM groups
GROUP BY customer_group