
WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, ROUND(AVG(cost),0) AS avg_monthly_cost, ROUND(SUM(cost),0) AS total_cost,
  ROUND(AVG(roas),3) AS avg_roas, ROUND(AVG(quality_score),2) AS avg_qs,
  ROUND(AVG(impression_share),3) AS avg_is, ROUND(AVG(ctr),5) AS avg_ctr,
  ROUND(AVG(conversion_rate),5) AS avg_cvr, ROUND(AVG(cpc),2) AS avg_cpc,
  ROUND(AVG(cost_per_conversion),2) AS avg_cpa,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score
