
SELECT g.year_month, g.campaign_id, g.geo_target, g.cost, g.roas, g.quality_score,
  g.impression_share, g.ctr, g.conversion_rate, g.conversions, g.conversion_value,
  g.cpc, g.cost_per_conversion
FROM google_ads__geo_report g
ORDER BY g.campaign_id, g.year_month, g.geo_target
