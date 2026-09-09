-- Search terms for problematic ad groups
SELECT s.ad_group_id, s.search_term, s.keyword_text, s.keyword_match_type, s.search_term_match_type,
       SUM(s.impressions) AS s_impressions, SUM(s.clicks) AS s_clicks, SUM(s.spend) AS s_spend, SUM(s.conversions) AS s_conversions
FROM google_ads__search_term_report s
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON s.ad_group_id = p.ad_group_id
GROUP BY s.ad_group_id, s.search_term, s.keyword_text, s.keyword_match_type, s.search_term_match_type
ORDER BY s.ad_group_id, s_impressions DESC