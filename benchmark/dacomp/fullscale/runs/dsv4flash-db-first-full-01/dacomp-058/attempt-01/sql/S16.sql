SELECT 
  COUNT(*) AS total,
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS roas_lt_08,
  ROUND(100.0 * COUNT(CASE WHEN roas < 0.8 THEN 1 END) / COUNT(*), 1) AS pct_lt_08
FROM google_ads__campaign_report