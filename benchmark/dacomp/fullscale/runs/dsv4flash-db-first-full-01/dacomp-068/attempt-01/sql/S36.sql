-- Full market segment analysis
SELECT 
  g.package_name,
  g.country,
  g.country_name,
  g.region,
  g.sub_region,
  g.avg_daily_revenue,
  g.store_conversion_rate,
  g.revenue_last_30_days,
  g.store_visitors_30d,
  g.store_installs_30d,
  g.avg_transaction_value,
  g.average_revenue_per_user,
  g.market_tier,
  g.opportunity_type,
  g.investment_recommendation,
  g.revenue_opportunity_score,
  g.growth_potential_score,
  g.overall_market_score,
  CASE 
    WHEN g.store_conversion_rate > 15 AND g.avg_daily_revenue < 5 THEN 'Segment A: High Conv, Low Rev'
    WHEN g.avg_daily_revenue > 7 AND g.store_conversion_rate < 10 THEN 'Segment B: High Rev, Low Conv'
    ELSE 'Other'
  END AS market_segment
FROM google_play__geo_market_analysis g
ORDER BY market_segment, g.package_name, g.country