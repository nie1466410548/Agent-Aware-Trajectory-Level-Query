WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
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
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT is_target,
  COUNT(*) AS n,
  SUM(acquisition_cost) AS total_acq_cost,
  SUM(customer_lifetime_value) AS total_clv,
  SUM(total_sales_amount) AS total_sales,
  ROUND(100.0*SUM(acquisition_cost)/ (SELECT SUM(acquisition_cost) FROM flagged), 1) AS pct_of_total_acq,
  ROUND(100.0*SUM(customer_lifetime_value)/ (SELECT SUM(customer_lifetime_value) FROM flagged), 1) AS pct_of_total_clv,
  ROUND(100.0*SUM(total_sales_amount)/ (SELECT SUM(total_sales_amount) FROM flagged), 1) AS pct_of_total_sales
FROM flagged
GROUP BY is_target