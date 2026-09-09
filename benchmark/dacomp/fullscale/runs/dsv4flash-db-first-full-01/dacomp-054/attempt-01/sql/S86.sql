-- Cohort by lifecycle_stage
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
  SELECT a.primary_email, f.customer_tier,
         a.customer_segment, a.lifecycle_stage,
         v.rfm_segment, v.rfm_score,
         a.customer_health_score, f.estimated_customer_ltv AS funnel_ltv
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT lifecycle_stage, COUNT(*) AS cnt, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM cohort),2) AS pct
FROM cohort GROUP BY lifecycle_stage ORDER BY cnt DESC