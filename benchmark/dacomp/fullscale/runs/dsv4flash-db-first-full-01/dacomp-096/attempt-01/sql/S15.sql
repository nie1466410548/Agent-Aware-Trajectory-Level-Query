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
    CASE WHEN count_received_email < 10000 THEN '<10k'
         WHEN count_received_email <= 100000 THEN '10k-100k'
         ELSE '>100k' END AS audience_bucket,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
  WHERE created_at >= '2023-02-27'
),
stats AS (
  SELECT campaign_type, audience_bucket, COUNT(*) AS n_hist,
    AVG(or_calc) AS mu_or,
    AVG(ctor_calc) AS mu_ctor,
    SQRT( (SUM(or_calc*or_calc) - SUM(or_calc)*SUM(or_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_or,
    SQRT( (SUM(ctor_calc*ctor_calc) - SUM(ctor_calc)*SUM(ctor_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_ctor
  FROM base
  GROUP BY campaign_type, audience_bucket
)
SELECT * FROM stats ORDER BY campaign_type