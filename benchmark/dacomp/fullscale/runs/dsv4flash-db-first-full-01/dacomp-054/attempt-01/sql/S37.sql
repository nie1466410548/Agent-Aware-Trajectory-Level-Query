-- Calculate LTV difference vs others in same tier
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
combined AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         v.recency_score, v.frequency_score, v.monetary_score,
         v.estimated_customer_ltv AS value_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
),
cohort AS (
  SELECT * FROM combined
  WHERE marketing_to_sales_days BETWEEN 10 AND 20
    AND sales_to_support_days > 30
    AND composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
),
tier_avg_ltv AS (
  SELECT customer_tier, AVG(funnel_ltv) AS tier_avg_ltv
  FROM combined
  GROUP BY customer_tier
)
SELECT c.customer_tier, 
       COUNT(*) AS cohort_in_tier,
       AVG(c.funnel_ltv) AS cohort_avg_ltv,
       AVG(t.tier_avg_ltv) AS tier_avg_ltv,
       AVG(c.funnel_ltv) - AVG(t.tier_avg_ltv) AS ltv_difference
FROM cohort c
JOIN tier_avg_ltv t ON c.customer_tier = t.customer_tier
GROUP BY c.customer_tier
ORDER BY c.customer_tier