WITH agg AS (
  SELECT ad_group_id,
         SUM(clicks) AS clicks,
         SUM(impressions) AS impressions,
         SUM(conversions) AS conversions,
         SUM(spend) AS spend,
         SUM(conversions_value) AS conv_value
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
),
metrics AS (
  SELECT ad_group_id, clicks, impressions, conversions, spend, conv_value,
         clicks*1.0/impressions AS ctr,
         conversions*1.0/clicks AS cvr
  FROM agg
)
SELECT COUNT(*) AS total,
       SUM(CASE WHEN ctr > 0.035874 AND cvr < 0.038462 THEN 1 ELSE 0 END) AS problem_count
FROM metrics