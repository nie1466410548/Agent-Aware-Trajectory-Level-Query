-- RFM segment distribution in cohort
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
  SELECT a.primary_email, f.customer_tier, v.rfm_segment, v.rfm_score,
         v.recency_score, v.frequency_score, v.monetary_score,
         a.customer_health_score, f.estimated_customer_ltv AS funnel_ltv,
         a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT rfm_segment, COUNT(*) AS cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
       ROUND(AVG(recency_score), 1) AS avg_recency,
       ROUND(AVG(frequency_score), 1) AS avg_frequency,
       ROUND(AVG(monetary_score), 1) AS avg_monetary,
       ROUND(AVG(funnel_ltv), 0) AS avg_ltv,
       ROUND(AVG(customer_health_score), 1) AS avg_health
FROM cohort
GROUP BY rfm_segment
ORDER BY cnt DESC