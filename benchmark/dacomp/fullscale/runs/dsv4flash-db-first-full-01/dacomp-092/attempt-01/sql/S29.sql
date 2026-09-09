-- Compute coefficient of variation of gross_profit for high-vol customers over past 12 months
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
stats AS (
  SELECT 
    h.customer_id,
    h.vol,
    AVG(p.gross_profit) AS mean_gp,
    AVG(p.gross_profit * p.gross_profit) - AVG(p.gross_profit) * AVG(p.gross_profit) AS var_gp,
    COUNT(p.gross_profit) AS n_obs
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, h.vol
)
SELECT 
  customer_id, vol, mean_gp,
  CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END AS std_gp,
  CASE WHEN mean_gp = 0 THEN NULL 
       ELSE CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END / mean_gp END AS cv_gp,
  n_obs
FROM stats
ORDER BY vol DESC
LIMIT 20