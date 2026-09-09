WITH base_all AS (
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
),
stats AS (
  SELECT campaign_type, audience_bucket,
    AVG(or_calc) AS mu_or,
    AVG(ctor_calc) AS mu_ctor,
    SQRT( (SUM(or_calc*or_calc) - SUM(or_calc)*SUM(or_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_or,
    SQRT( (SUM(ctor_calc*ctor_calc) - SUM(ctor_calc)*SUM(ctor_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_ctor
  FROM base_all
  WHERE created_at >= '2023-02-27'
  GROUP BY campaign_type, audience_bucket
),
prev_updated AS (
  SELECT flow_id, flow_name, campaign_type, audience_bucket, created_at, updated_at,
    status, variation_id, source_relation, or_calc, ctor_calc,
    LAG(updated_at) OVER (ORDER BY updated_at) AS prev_updated_at
  FROM base_all
),
anomalies AS (
  SELECT p.*, s.mu_or, s.mu_ctor, s.sd_or, s.sd_ctor,
    CASE WHEN p.or_calc < s.mu_or - 2*s.sd_or OR p.or_calc > s.mu_or + 2*s.sd_or THEN 1 ELSE 0 END AS or_anomaly,
    CASE WHEN p.ctor_calc < s.mu_ctor - 2*s.sd_ctor OR p.ctor_calc > s.mu_ctor + 2*s.sd_ctor THEN 1 ELSE 0 END AS ctor_anomaly,
    CASE WHEN prev_updated_at IS NOT NULL AND (julianday(p.updated_at) - julianday(p.prev_updated_at))*24 < 24 THEN 1 ELSE 0 END AS freq_anomaly
  FROM prev_updated p
  LEFT JOIN stats s ON p.campaign_type = s.campaign_type AND p.audience_bucket = s.audience_bucket
)
SELECT flow_id, flow_name, campaign_type, audience_bucket, 
  created_at, updated_at, prev_updated_at,
  ROUND(CAST((julianday(updated_at) - julianday(prev_updated_at))*24 AS REAL),2) AS hours_since_prev,
  or_calc, mu_or, sd_or, or_anomaly,
  ctor_calc, mu_ctor, sd_ctor, ctor_anomaly,
  freq_anomaly,
  CASE WHEN or_anomaly=1 OR ctor_anomaly=1 OR freq_anomaly=1 THEN 1 ELSE 0 END AS any_anomaly
FROM anomalies
ORDER BY any_anomaly DESC, freq_anomaly DESC, or_anomaly DESC, ctor_anomaly DESC