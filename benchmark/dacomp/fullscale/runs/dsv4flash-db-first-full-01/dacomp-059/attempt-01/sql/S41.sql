WITH master AS (
  SELECT r.ad_group_id, r.account_name,
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
SELECT industry,
       COUNT(*) AS total,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)/SUM(clicks),1) AS pct_clicks,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)/SUM(spend),1) AS pct_spend
FROM master GROUP BY industry ORDER BY problem_pct DESC