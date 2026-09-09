WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name, r.campaign_id, r.ad_group_type, r.status,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         CASE
           WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
           WHEN r.account_name LIKE '%Education%' THEN 'Education'
           WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
           WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
           WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
           WHEN r.account_name LIKE '%Food%' THEN 'Food'
           WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
           WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
           WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
           WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
           WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
           WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
           ELSE 'Other'
         END AS industry
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT (ctr > 0.0358744 AND cvr < 0.0384615) AS is_problem,
       COUNT(*) AS ad_groups,
       SUM(clicks) AS clicks, SUM(impressions) AS impressions,
       SUM(conversions) AS conversions, ROUND(SUM(spend),2) AS spend,
       ROUND(100.0*SUM(clicks)/SUM(impressions),3) AS ctr_pct,
       ROUND(100.0*SUM(conversions)/SUM(clicks),3) AS cvr_pct
FROM master
GROUP BY is_problem