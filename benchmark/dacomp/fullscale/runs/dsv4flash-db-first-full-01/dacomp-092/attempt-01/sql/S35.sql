-- Variance of QoQ invoice_total growth rate for high-vol customers
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
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  AVG(qoq_growth) AS mean_qoq_growth,
  AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth) AS var_qoq_growth,
  SQRT(AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth)) AS std_qoq_growth,
  COUNT(*) AS n_obs
FROM (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total, prev_qtr_total,
    CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
         THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
  FROM qoqs
  WHERE prev_qtr_total IS NOT NULL
) WHERE qoq_growth IS NOT NULL