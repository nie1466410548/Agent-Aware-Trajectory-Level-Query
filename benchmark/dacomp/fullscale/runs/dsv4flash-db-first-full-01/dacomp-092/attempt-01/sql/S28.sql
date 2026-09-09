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
)
SELECT 
  h.customer_id,
  h.vol,
  AVG(p.gross_profit) AS mean_gross_profit,
  STDEV(p.gross_profit) AS std_gross_profit,
  CASE WHEN AVG(p.gross_profit) = 0 THEN NULL 
       ELSE STDEV(p.gross_profit) / AVG(p.gross_profit) END AS cv_gross_profit,
  COUNT(p.gross_profit) AS n_obs
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
  AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY h.customer_id, h.vol
ORDER BY h.vol DESC
LIMIT 20