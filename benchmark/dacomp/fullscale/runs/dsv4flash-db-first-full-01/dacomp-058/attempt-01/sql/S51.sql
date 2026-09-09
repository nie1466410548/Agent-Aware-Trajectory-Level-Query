
SELECT year_month, ROUND(SUM(cost),0) AS total_cost, ROUND(SUM(conversion_value),0) AS total_cv,
  ROUND(SUM(conversions),2) AS total_conv, ROUND(AVG(roas),3) AS avg_roas
FROM google_ads__campaign_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY year_month ORDER BY year_month
