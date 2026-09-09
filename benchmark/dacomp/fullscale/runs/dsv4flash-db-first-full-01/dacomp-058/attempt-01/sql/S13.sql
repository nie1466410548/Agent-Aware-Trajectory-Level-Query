-- Check cost distribution
SELECT 
  CASE 
    WHEN cost < 5000 THEN '0-5K'
    WHEN cost < 10000 THEN '5K-10K'
    WHEN cost < 30000 THEN '10K-30K'
    WHEN cost < 50000 THEN '30K-50K'
    WHEN cost < 100000 THEN '50K-100K'
    ELSE '100K+'
  END AS cost_range,
  COUNT(*) AS n_months,
  ROUND(AVG(conversion_value/NULLIF(cost,0)),3) AS avg_roi,
  ROUND(AVG(roas),3) AS avg_roas
FROM google_ads__campaign_report
GROUP BY cost_range
ORDER BY MIN(cost)