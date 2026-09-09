
SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  cost, roas, quality_score, impression_share, ctr, conversion_rate, conversions, conversion_value
FROM google_ads__campaign_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
ORDER BY campaign_id, year_month
