-- Segment-level summary
WITH seg AS (
  SELECT package_name, country,
    CASE 
      WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 'A_HighConv_LowRev'
      WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 'B_HighRev_LowConv'
      ELSE 'Other'
    END AS seg
  FROM google_play__geo_market_analysis
)
SELECT seg,
  COUNT(*) AS n_markets,
  COUNT(DISTINCT package_name) AS n_apps,
  SUM(g.store_visitors_30d) AS total_visitors,
  SUM(g.store_installs_30d) AS total_installs,
  SUM(g.revenue_last_30_days) AS total_rev_30d,
  ROUND(AVG(g.store_conversion_rate), 2) AS avg_conv,
  ROUND(AVG(g.avg_daily_revenue), 2) AS avg_daily_rev
FROM seg s JOIN google_play__geo_market_analysis g ON s.package_name = g.package_name AND s.country = g.country
GROUP BY seg
ORDER BY seg