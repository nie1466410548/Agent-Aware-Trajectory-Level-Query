SELECT DISTINCT flow_name,
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