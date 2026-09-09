-- URL report for problematic ad groups
SELECT u.ad_group_id, u.base_url, u.url_host, u.url_path,
       SUM(u.impressions) AS u_impressions, SUM(u.clicks) AS u_clicks, SUM(u.spend) AS u_spend, SUM(u.conversions) AS u_conversions
FROM google_ads__url_report u
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON u.ad_group_id = p.ad_group_id
GROUP BY u.ad_group_id, u.base_url, u.url_host, u.url_path
ORDER BY u.ad_group_id, u_impressions DESC