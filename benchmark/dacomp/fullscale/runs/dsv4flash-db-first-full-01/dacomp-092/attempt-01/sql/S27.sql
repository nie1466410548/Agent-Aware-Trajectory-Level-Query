-- Define the past 12 months date range
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
-- High volatility customers (top 25%)
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
-- Get gross_profit data for past 12 months
SELECT h.customer_id, h.vol, p.gross_profit, p.transaction_date
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
WHERE p.transaction_date >= (SELECT cutoff_date FROM date_range)
ORDER BY h.vol DESC, h.customer_id, p.transaction_date
LIMIT 20