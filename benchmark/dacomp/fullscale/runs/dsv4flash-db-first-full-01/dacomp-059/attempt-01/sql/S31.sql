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
),
ranked AS (
  SELECT m.*,
         ROW_NUMBER() OVER (ORDER BY ctr) AS rn_ctr,
         ROW_NUMBER() OVER (ORDER BY cvr) AS rn_cvr,
         COUNT(*) OVER () AS n
  FROM metrics m
)
SELECT ctr_value, cvr_value, n
FROM (
  SELECT ctr AS ctr_value, rn_ctr, n FROM ranked WHERE rn_ctr = CAST(0.75*n AS INTEGER)
) AS ctr_t
CROSS JOIN (
  SELECT cvr AS cvr_value, rn_cvr FROM ranked WHERE rn_cvr = CAST(0.25*n AS INTEGER)
) AS cvr_t