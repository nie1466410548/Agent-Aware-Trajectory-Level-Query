-- All search terms data
SELECT s.ad_group_id, s.search_term, s.keyword_match_type, s.search_term_match_type,
       SUM(s.impressions) AS s_impressions, SUM(s.clicks) AS s_clicks, SUM(s.spend) AS s_spend, SUM(s.conversions) AS s_conversions
FROM google_ads__search_term_report s
GROUP BY s.ad_group_id, s.search_term, s.keyword_match_type, s.search_term_match_type