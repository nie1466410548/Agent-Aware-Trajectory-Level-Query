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
    CASE WHEN CAST(strftime('%w', created_at) AS INT) IN (0,6) THEN 'Weekend' ELSE 'Weekday' END AS weekday_flag,
    CASE WHEN CAST(strftime('%H', created_at) AS INT) < 12 THEN 'Morning' ELSE 'Afternoon' END AS daypart,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, weekday_flag, daypart, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, weekday_flag, daypart
ORDER BY campaign_type, weekday_flag, daypart