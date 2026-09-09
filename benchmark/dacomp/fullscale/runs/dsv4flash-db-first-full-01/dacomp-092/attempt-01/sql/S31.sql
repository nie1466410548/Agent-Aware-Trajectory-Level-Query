-- Overall CV of monthly gross profit for high-volatility customers
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
)
SELECT 
  AVG(monthly_gp) AS overall_mean_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) AS overall_std_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) / ABS(AVG(monthly_gp)) AS overall_cv_gp,
  COUNT(*) AS total_month_obs,
  COUNT(DISTINCT customer_id) AS n_customers_with_data
FROM monthly