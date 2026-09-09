WITH base AS (
  SELECT 
    year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT b.*,
    (b.roas - MIN(b.roas) OVER()) / NULLIF(MAX(b.roas) OVER() - MIN(b.roas) OVER(), 0) AS roas_s,
    (MAX(b.cpc) OVER() - b.cpc) / NULLIF(MAX(b.cpc) OVER() - MIN(b.cpc) OVER(), 0) AS cpc_s,
    (MAX(b.cost_per_conversion) OVER() - b.cost_per_conversion) / NULLIF(MAX(b.cost_per_conversion) OVER() - MIN(b.cost_per_conversion) OVER(), 0) AS cpa_s,
    (b.conversion_rate - MIN(b.conversion_rate) OVER()) / NULLIF(MAX(b.conversion_rate) OVER() - MIN(b.conversion_rate) OVER(), 0) AS cvr_s,
    (b.conversion_value/NULLIF(b.conversions,0) - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER()) / NULLIF(MAX(b.conversion_value/NULLIF(b.conversions,0)) OVER() - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER(), 0) AS aov_s,
    (b.conversions - MIN(b.conversions) OVER()) / NULLIF(MAX(b.conversions) OVER() - MIN(b.conversions) OVER(), 0) AS conv_s,
    (b.quality_score - MIN(b.quality_score) OVER()) / NULLIF(MAX(b.quality_score) OVER() - MIN(b.quality_score) OVER(), 0) AS qs_s,
    (b.impression_share - MIN(b.impression_share) OVER()) / NULLIF(MAX(b.impression_share) OVER() - MIN(b.impression_share) OVER(), 0) AS is_s,
    (b.ctr - MIN(b.ctr) OVER()) / NULLIF(MAX(b.ctr) OVER() - MIN(b.ctr) OVER(), 0) AS ctr_s
  FROM base b
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  ROUND(AVG(cost), 0) AS avg_monthly_cost,
  ROUND(SUM(cost), 0) AS total_cost,
  ROUND(AVG(roas), 3) AS avg_roas,
  ROUND(100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s), 2) AS cost_eff,
  ROUND(100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s), 2) AS conv_quality,
  ROUND(100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s), 2) AS competitive,
  ROUND(100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)), 2) AS health_score
FROM norm
GROUP BY campaign_id
ORDER BY health_score ASC