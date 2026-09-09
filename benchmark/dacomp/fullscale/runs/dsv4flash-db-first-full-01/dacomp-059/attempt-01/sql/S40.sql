WITH k AS (
  SELECT ad_group_id, keyword_match_type, SUM(clicks) AS clicks, SUM(impressions) AS imp, SUM(conversions) AS conv, SUM(spend) AS spend
  FROM google_ads__keyword_report GROUP BY ad_group_id, keyword_match_type
),
agg AS (
  SELECT ad_group_id, SUM(clicks) AS clicks, SUM(impressions) AS impressions, SUM(conversions) AS conversions
  FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING SUM(clicks)>0 AND SUM(impressions)>0
),
m AS (
  SELECT a.ad_group_id, a.clicks, a.impressions, a.conversions,
         a.clicks*1.0/a.impressions AS ctr, a.conversions*1.0/a.clicks AS cvr
  FROM agg a
),
flag AS (
  SELECT m.*, (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) AS is_problem FROM m
)
SELECT k.keyword_match_type, f.is_problem,
       COUNT(DISTINCT f.ad_group_id) AS ad_groups,
       SUM(k.clicks) AS clicks, SUM(k.conv) AS conv, ROUND(100.0*SUM(k.conv)/SUM(k.clicks),3) AS cvr_pct, ROUND(SUM(k.spend),2) AS spend
FROM k JOIN flag f ON k.ad_group_id = f.ad_group_id
GROUP BY k.keyword_match_type, f.is_problem
ORDER BY k.keyword_match_type, f.is_problem