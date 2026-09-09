-- High-vol customers' outstanding balance snapshot
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
high_vol_cust AS (
  SELECT customer_id FROM ordered WHERE rn <= total * 0.25
)
SELECT 
  CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END AS grp,
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.collected_amount) AS total_collected,
  COUNT(*) AS n_invoices,
  COUNT(DISTINCT p.customer_id) AS n_customers
FROM quickbooks__profitability_analysis p
LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
GROUP BY CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END