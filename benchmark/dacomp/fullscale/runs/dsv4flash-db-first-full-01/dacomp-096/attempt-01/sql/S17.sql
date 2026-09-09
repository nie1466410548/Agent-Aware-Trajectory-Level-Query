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
    END AS campaign_type
  FROM klaviyo__flows
),
template_stats AS (
  SELECT variation_id, campaign_type, COUNT(*) AS n_uses,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY campaign_type), 1) AS pct_of_type
  FROM base
  GROUP BY variation_id, campaign_type
)
SELECT * FROM template_stats ORDER BY campaign_type, n_uses DESC