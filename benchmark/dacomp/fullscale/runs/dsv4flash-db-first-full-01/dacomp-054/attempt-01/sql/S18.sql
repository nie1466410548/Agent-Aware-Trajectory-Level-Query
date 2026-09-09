SELECT a.primary_email, a.composite_engagement_score, f.marketing_to_sales_days, f.sales_to_support_days
FROM customer360__customer_activity_metrics a
INNER JOIN customer360__conversion_funnel_analysis f ON a.primary_email = f.primary_email
WHERE f.marketing_to_sales_days BETWEEN 10 AND 20
  AND f.sales_to_support_days > 30
  AND a.composite_engagement_score > 8.99949618540379
LIMIT 20