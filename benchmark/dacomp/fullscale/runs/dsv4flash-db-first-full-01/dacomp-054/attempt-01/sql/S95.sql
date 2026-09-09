-- Full risk-velocity breakdown
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
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.cross_platform_consistency, a.activity_efficiency,
         a.days_since_last_activity, a.estimated_monthly_activities,
         v.rfm_segment, v.churn_probability, v.investment_priority_score,
         v.risk_category, v.rfm_score, v.recency_score, v.frequency_score, v.monetary_score
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  activity_risk_level,
  engagement_velocity,
  COUNT(*) AS cnt,
  ROUND(AVG(customer_health_score), 1) AS avg_health,
  ROUND(AVG(funnel_ltv), 0) AS avg_ltv,
  ROUND(AVG(composite_engagement_score), 1) AS avg_engagement,
  ROUND(AVG(churn_probability), 3) AS avg_churn_prob,
  ROUND(AVG(cross_platform_consistency), 3) AS avg_platform_consistency,
  ROUND(AVG(days_since_last_activity), 0) AS avg_days_since_activity
FROM cohort
GROUP BY activity_risk_level, engagement_velocity
ORDER BY activity_risk_level, engagement_velocity