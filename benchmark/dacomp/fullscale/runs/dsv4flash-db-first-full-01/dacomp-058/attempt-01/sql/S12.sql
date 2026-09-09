SELECT
  MIN(roas) AS min_roas, 
  MAX(roas) AS max_roas,
  AVG(roas) AS avg_roas,
  MIN(conversion_value/NULLIF(cost,0)) AS min_roi_cv,
  MAX(conversion_value/NULLIF(cost,0)) AS max_roi_cv,
  AVG(conversion_value/NULLIF(cost,0)) AS avg_roi_cv,
  AVG(cost) AS avg_cost,
  MIN(cost) AS min_cost,
  MAX(cost) AS max_cost
FROM google_ads__campaign_report