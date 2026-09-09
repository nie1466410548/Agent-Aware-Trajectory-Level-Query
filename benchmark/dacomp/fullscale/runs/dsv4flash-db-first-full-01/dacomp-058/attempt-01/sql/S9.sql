SELECT
  campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  SUM(cost) AS total_cost,
  SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0),4) AS roi,
  ROUND(AVG(quality_score),2) AS avg_qs,
  ROUND(AVG(impression_share),3) AS avg_is,
  ROUND(AVG(ctr),4) AS avg_ctr,
  ROUND(AVG(conversion_rate),4) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY total_cost DESC