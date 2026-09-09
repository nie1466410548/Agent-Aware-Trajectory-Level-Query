-- Monthly cost > 1000 and ROI < 0.8 (using conversion_value/cost as ROI)
SELECT cr.*, ROUND(cr.conversion_value/NULLIF(cr.cost,0),4) AS roi
FROM google_ads__campaign_report cr
WHERE cr.cost > 1000
  AND (cr.conversion_value/NULLIF(cr.cost,0)) < 0.8
ORDER BY cr.cost DESC