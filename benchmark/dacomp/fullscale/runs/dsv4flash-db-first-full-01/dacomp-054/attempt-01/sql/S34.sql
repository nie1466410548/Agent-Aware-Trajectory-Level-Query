-- Get the latest funnel record per email
SELECT primary_email, marketing_to_sales_days, sales_to_support_days, customer_tier, estimated_customer_ltv
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
) WHERE rn = 1
LIMIT 10