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
    SUBSTR(flow_name, INSTR(flow_name,'Variant ')+8, 1) AS variant_letter,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, variant_letter, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, variant_letter
ORDER BY campaign_type, variant_letter