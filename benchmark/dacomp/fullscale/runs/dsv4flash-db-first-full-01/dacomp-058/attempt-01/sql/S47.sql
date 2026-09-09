
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS total_months,
  COUNT(CASE WHEN cost > 1000 AND roas < 0.8 THEN 1 END) AS screened_months
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY screened_months DESC
