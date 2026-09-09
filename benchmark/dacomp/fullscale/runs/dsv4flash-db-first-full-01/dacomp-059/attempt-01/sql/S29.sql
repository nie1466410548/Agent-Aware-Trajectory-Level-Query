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
SELECT 'ctr_p75' AS metric, MIN(ctr) AS value, MAX(rn_ctr) AS rank FROM ranked WHERE rn_ctr >= CAST(0.75*n AS INT) AND rn_ctr <= CAST(0.75*n AS INT)+1
UNION ALL
SELECT 'ctr_p25', MIN(ctr), MAX(rn_ctr) FROM ranked WHERE rn_ctr >= CAST(0.25*n AS INT) AND rn_ctr <= CAST(0.25*n AS INT)+1
UNION ALL
SELECT 'cvr_p75', MIN(cvr), MAX(rn_cvr) FROM ranked WHERE rn_cvr >= CAST(0.75*n AS INT) AND rn_cvr <= CAST(0.75*n AS INT)+1
UNION ALL
SELECT 'cvr_p25', MIN(cvr), MAX(rn_cvr) FROM ranked WHERE rn_cvr >= CAST(0.25*n AS INT) AND rn_cvr <= CAST(0.25*n AS INT)+1
UNION ALL
SELECT 'n', MIN(n), MAX(n) FROM ranked