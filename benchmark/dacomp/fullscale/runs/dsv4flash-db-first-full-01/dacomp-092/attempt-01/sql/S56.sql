-- Outstanding balance by volatility segment
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
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.collected_amount) AS total_collected,
  ROUND(100.0 * SUM(p.outstanding_balance) / NULLIF(SUM(p.invoice_total), 0), 2) AS outstanding_ratio,
  COUNT(DISTINCT s.customer_id) AS n_customers
FROM seg s
JOIN quickbooks__profitability_analysis p ON s.customer_id = p.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment