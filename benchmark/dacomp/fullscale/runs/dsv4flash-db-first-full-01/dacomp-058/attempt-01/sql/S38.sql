
SELECT d.year_month, d.campaign_id, d.device_type, d.cost, d.roas, d.quality_score, 
  d.impression_share, d.ctr, d.conversion_rate, d.conversions, d.conversion_value,
  d.cpc, d.cost_per_conversion
FROM google_ads__device_report d
ORDER BY d.campaign_id, d.year_month, d.device_type
