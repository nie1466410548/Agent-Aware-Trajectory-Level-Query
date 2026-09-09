
SELECT year_month, 
  SUM(cost) AS total_cost,
  SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv,
  AVG(roas) AS avg_roas,
  AVG(quality_score) AS avg_qs,
  AVG(impression_share) AS avg_is,
  AVG(ctr) AS avg_ctr,
  AVG(conversion_rate) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY year_month
ORDER BY year_month
