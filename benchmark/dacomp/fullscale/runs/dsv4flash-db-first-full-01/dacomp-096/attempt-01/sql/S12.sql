WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE
      WHEN flow_name IN ('Cart Recovery Series - Variant A','Cart Recovery Series - Variant B','Cart Recovery Series - Variant C',
                         'Seasonal Warmup Flow - Variant A','Seasonal Warmup Flow - Variant B','Seasonal Warmup Flow - Variant C',
                         'Winback Journey - Variant A','Winback Journey - Variant B','Winback Journey - Variant C',
                         'Browse Abandonment - Variant A','Browse Abandonment - Variant B','Browse Abandonment - Variant C') THEN 'Promotional'
      WHEN flow_name LIKE 'Product Discovery%' OR flow_name LIKE 'Welcome%' THEN 'New Product'
      WHEN flow_name LIKE 'Post-Purchase%' OR flow_name LIKE 'VIP Loyalty%' THEN 'Storytelling'
      ELSE 'Other'
    END AS category_3,
    CASE WHEN count_received_email < 10000 THEN '<10k'
         WHEN count_received_email <= 100000 THEN '10k-100k'
         ELSE '>100k' END AS audience_bucket,
    CAST(strftime('%Y-%m-%d', created_at) AS TEXT) AS sent_date,
    strftime('%H', created_at) AS hour_sent,
    CAST(julianday(created_at) - julianday('2023-01-01') AS INT) % 7 AS day_of_week,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, category_3, audience_bucket, COUNT(*) AS n,
  MIN(count_received_email) AS min_aud, MAX(count_received_email) AS max_aud,
  ROUND(AVG(or_calc),4) AS mean_or, ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, category_3, audience_bucket
ORDER BY category_3, campaign_type