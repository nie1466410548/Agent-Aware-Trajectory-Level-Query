-- Compare CV for bottom 25% (low volatility) customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol ASC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
low_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT COUNT(*) AS n_low_vol FROM low_vol_cust