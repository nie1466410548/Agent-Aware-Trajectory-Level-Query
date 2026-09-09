-- Profitability sustainability by volatility segment
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
  p.profitability_sustainability,
  COUNT(*) AS n_rows,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY s.vol_segment), 1) AS pct
FROM seg s
JOIN quickbooks__profitability_analysis p ON s.customer_id = p.customer_id
GROUP BY s.vol_segment, p.profitability_sustainability
ORDER BY s.vol_segment, pct DESC