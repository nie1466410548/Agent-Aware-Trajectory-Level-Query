-- Monthly gross profit per high-vol customer over past 12 months, then CV
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
),
stats AS (
  SELECT 
    customer_id,
    AVG(monthly_gp) AS mean_mgp,
    AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp) AS var_mgp,
    COUNT(*) AS n_months
  FROM monthly
  GROUP BY customer_id
)
SELECT 
  customer_id,
  mean_mgp,
  CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END AS std_mgp,
  CASE WHEN mean_mgp = 0 THEN NULL 
       ELSE CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END / ABS(mean_mgp) END AS cv_mgp,
  n_months
FROM stats
ORDER BY cv_mgp DESC NULLS LAST
LIMIT 15