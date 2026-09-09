WITH master AS (
  SELECT r.ad_group_id, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         CASE
           WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
           WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
           WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
           WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
           WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
         END AS channel,
         CASE
           WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
           WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
           WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
           WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
           WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
         END AS strategy
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT strategy,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS non_problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)/SUM(clicks),1) AS pct_of_clicks,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)/SUM(spend),1) AS pct_of_spend
FROM master GROUP BY strategy ORDER BY problem_pct DESC