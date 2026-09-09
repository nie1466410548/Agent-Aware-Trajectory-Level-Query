WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target,
    CASE WHEN team_size <= 2 THEN '1-2' WHEN team_size <= 5 THEN '3-5' WHEN team_size <= 10 THEN '6-10' WHEN team_size <= 20 THEN '11-20' ELSE '20+' END AS team_bucket
  FROM ranked
)
SELECT team_bucket,
  COUNT(*) AS total_cnt,
  SUM(is_target) AS cohort_cnt,
  ROUND(100.0*SUM(is_target)/COUNT(*), 1) AS cohort_pct,
  AVG(CASE WHEN is_target=1 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS cohort_avg_roi,
  AVG(CASE WHEN is_target=0 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS noncohort_avg_roi,
  AVG(CASE WHEN is_target=1 THEN product_adoption_rate END) AS cohort_avg_par,
  AVG(CASE WHEN is_target=0 THEN product_adoption_rate END) AS noncohort_avg_par
FROM flagged
WHERE team_size IS NOT NULL
GROUP BY team_bucket
ORDER BY MIN(team_size)