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
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT variation_id, campaign_type, COUNT(*) AS n_uses,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY campaign_type), 1) AS pct_of_type,
  ROUND(AVG(or_calc),4) AS avg_or,
  ROUND(AVG(ctor_calc),4) AS avg_ctor
FROM base
GROUP BY variation_id, campaign_type
ORDER BY pct_of_type DESC, avg_ctor DESC