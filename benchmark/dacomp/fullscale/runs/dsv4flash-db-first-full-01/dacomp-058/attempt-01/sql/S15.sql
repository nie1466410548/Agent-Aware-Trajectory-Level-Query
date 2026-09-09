-- Count of months with roas<0.8 grouped by campaign
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS bad_months, 
  COUNT(CASE WHEN roas >= 0.8 THEN 1 END) AS good_months,
  ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(conversion_value/NULLIF(cost,0)),3) AS avg_cv_ratio
FROM google_ads__campaign_report
WHERE roas < 0.8
GROUP BY campaign_id
ORDER BY bad_months DESC