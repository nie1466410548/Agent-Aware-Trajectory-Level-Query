-- All keywords with match type distribution per ad group
SELECT k.ad_group_id, k.keyword_match_type, k.type, k.status AS kw_status,
       SUM(k.impressions) AS kw_impressions, SUM(k.clicks) AS kw_clicks, SUM(k.spend) AS kw_spend, SUM(k.conversions) AS kw_conversions
FROM google_ads__keyword_report k
GROUP BY k.ad_group_id, k.keyword_match_type, k.type, k.status