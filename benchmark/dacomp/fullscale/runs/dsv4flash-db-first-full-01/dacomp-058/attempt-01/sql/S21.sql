-- Campaign-level summary with all metrics needed
SELECT 
  campaign_id,
  campaign_name,
  campaign_type,
  bidding_strategy,
  industry,
  COUNT(*) AS n_months,
  MIN(year_month) AS first_month,
  MAX(year_month) AS last_month,
  ROUND(SUM(cost), 2) AS total_cost,
  ROUND(AVG(cost), 0) AS avg_monthly_cost,
  ROUND(SUM(conversions), 2) AS total_conversions,
  ROUND(SUM(conversion_value), 2) AS total_cv,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 4) AS overall_roi,
  ROUND(AVG(roas), 4) AS avg_roas,
  ROUND(AVG(quality_score), 2) AS avg_quality_score,
  ROUND(AVG(impression_share), 4) AS avg_impression_share,
  ROUND(AVG(ctr), 5) AS avg_ctr,
  ROUND(AVG(conversion_rate), 5) AS avg_conversion_rate,
  ROUND(AVG(cpc), 2) AS avg_cpc,
  ROUND(AVG(cost_per_conversion), 2) AS avg_cost_per_conv,
  -- Count of months with roas < 0.8
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS bad_roas_months,
  ROUND(100.0 * COUNT(CASE WHEN roas < 0.8 THEN 1 END) / COUNT(*), 1) AS pct_bad_roas
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY total_cost DESC