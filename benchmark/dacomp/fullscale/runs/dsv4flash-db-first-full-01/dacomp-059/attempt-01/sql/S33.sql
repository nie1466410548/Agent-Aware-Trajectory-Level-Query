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
SELECT ad_group_id, clicks, impressions, conversions, ROUND(ctr*100,4) AS ctr_pct, ROUND(cvr*100,4) AS cvr_pct, ROUND(spend,2) AS spend
FROM metrics
WHERE ctr > 0.035874 AND cvr < 0.038462
ORDER BY ctr DESC, cvr ASC
LIMIT 30