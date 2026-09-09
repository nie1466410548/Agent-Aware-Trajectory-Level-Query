
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
)
SELECT customer_id, vol,
  CASE WHEN rn <= total * 0.25 THEN 'HighVol'
       WHEN rn > total * 0.75 THEN 'LowVol'
       ELSE 'MidVol' END AS vol_segment
FROM ordered
