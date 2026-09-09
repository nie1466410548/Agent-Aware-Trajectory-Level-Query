SELECT package_name, country, avg_daily_revenue, store_conversion_rate,
  CASE 
    WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 'Segment A'
    WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 'Segment B'
    ELSE 'Other'
  END AS market_segment
FROM google_play__geo_market_analysis
WHERE package_name = 'com.studio.videostreaming'