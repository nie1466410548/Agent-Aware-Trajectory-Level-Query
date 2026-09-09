-- Customer value segment by volatility segment
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
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.customer_value_segment,
  COUNT(*) AS n_customers,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY s.vol_segment), 1) AS pct
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.customer_value_segment
ORDER BY s.vol_segment, n_customers DESC