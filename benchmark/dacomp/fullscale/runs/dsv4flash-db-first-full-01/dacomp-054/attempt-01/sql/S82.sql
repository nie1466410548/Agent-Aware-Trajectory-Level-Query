-- Multi-platform engagement patterns impact on customer_health_score
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
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  CASE 
    WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 1 THEN 'All 3 Platforms'
    WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Marketo + Stripe'
    WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Marketo + Zendesk'
    WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 1 THEN 'Stripe + Zendesk'
    WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 0 THEN 'Marketo Only'
    WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Stripe Only'
    WHEN in_marketo = 0 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Zendesk Only'
    ELSE 'None'
  END AS platform_pattern,
  COUNT(*) AS cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
  ROUND(AVG(customer_health_score), 2) AS avg_health_score,
  ROUND(AVG(composite_engagement_score), 2) AS avg_engagement_score,
  ROUND(AVG(funnel_ltv), 2) AS avg_ltv
FROM cohort
GROUP BY platform_pattern
ORDER BY cnt DESC