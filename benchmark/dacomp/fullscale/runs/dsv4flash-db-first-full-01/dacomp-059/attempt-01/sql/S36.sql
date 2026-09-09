WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT CASE
         WHEN campaign_name LIKE 'Brand%' THEN 'Brand'
         WHEN campaign_name LIKE 'Display%' THEN 'Display'
         WHEN campaign_name LIKE 'Performance%' THEN 'Performance'
         WHEN campaign_name LIKE 'Search%' THEN 'Search'
         WHEN campaign_name LIKE 'Shopping%' THEN 'Shopping'
       END AS channel,
       (ctr > 0.0358744 AND cvr < 0.0384615) AS is_problem,
       COUNT(*) AS ad_groups,
       ROUND(100.0*SUM(clicks)/SUM(impressions),3) AS ctr_pct,
       ROUND(100.0*SUM(conversions)/SUM(clicks),3) AS cvr_pct,
       ROUND(SUM(spend),2) AS spend
FROM master
GROUP BY channel, is_problem
ORDER BY channel, is_problem