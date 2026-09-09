-- Keywords for problematic ad groups: join with problematic list
SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.type, k.status AS kw_status,
       SUM(k.impressions) AS kw_impressions, SUM(k.clicks) AS kw_clicks, SUM(k.spend) AS kw_spend,
       SUM(k.conversions) AS kw_conversions
FROM google_ads__keyword_report k
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON k.ad_group_id = p.ad_group_id
GROUP BY k.ad_group_id, k.keyword_text, k.keyword_match_type
ORDER BY k.ad_group_id, kw_impressions DESC