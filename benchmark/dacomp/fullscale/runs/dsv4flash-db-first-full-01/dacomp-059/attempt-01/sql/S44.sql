WITH flag AS (
  SELECT ad_group_id,
         (SUM(clicks)*1.0/SUM(impressions) > 0.03587443946188341 AND SUM(conversions)*1.0/SUM(clicks) < 0.038461538461538464) AS is_problem
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
)
SELECT f.is_problem, k.keyword_match_type, COUNT(*) AS kw_rows, ROUND(SUM(k.clicks),0) AS clicks, ROUND(SUM(k.impressions),0) AS imp, ROUND(SUM(k.conversions),2) AS conv, ROUND(SUM(k.spend),2) AS spend
FROM google_ads__keyword_report k JOIN flag f ON k.ad_group_id = f.ad_group_id
GROUP BY f.is_problem, k.keyword_match_type
ORDER BY f.is_problem, k.keyword_match_type