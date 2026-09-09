WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT period,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS non_problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct
FROM master GROUP BY period ORDER BY problem_pct DESC