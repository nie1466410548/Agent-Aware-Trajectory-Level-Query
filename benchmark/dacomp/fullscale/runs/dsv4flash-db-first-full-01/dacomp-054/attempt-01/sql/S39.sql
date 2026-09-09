-- Overall average LTV difference
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
non_cohort_tier_avg AS (
  SELECT c2.customer_tier, AVG(c2.funnel_ltv) AS non_cohort_tier_avg_ltv
  FROM combined c2
  WHERE c2.primary_email NOT IN (SELECT primary_email FROM cohort)
  GROUP BY c2.customer_tier
)
SELECT AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv) AS overall_avg_ltv_diff
FROM cohort c
JOIN non_cohort_tier_avg t ON c.customer_tier = t.customer_tier