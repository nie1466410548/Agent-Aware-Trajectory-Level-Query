SELECT year_month, cost, conversions, conversion_value, roas, 
  ROUND(conversion_value/NULLIF(cost,0), 4) AS computed_roas
FROM google_ads__campaign_report
WHERE campaign_id = 69
ORDER BY year_month