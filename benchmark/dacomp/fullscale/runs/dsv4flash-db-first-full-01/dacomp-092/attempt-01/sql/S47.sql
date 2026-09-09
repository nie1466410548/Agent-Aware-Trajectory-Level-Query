-- Monthly contribution of high-vol customers vs overall, matched to dashboard months
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
),
monthly_seg AS (
  SELECT 
    p.revenue_month_start,
    CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END AS grp,
    SUM(p.invoice_total) AS invoice_total,
    SUM(p.gross_profit) AS gross_profit,
    SUM(p.outstanding_balance) AS outstanding
  FROM quickbooks__profitability_analysis p
  LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
  GROUP BY p.revenue_month_start, CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END
)
SELECT 
  m.revenue_month_start,
  SUM(CASE WHEN grp='HighVol' THEN invoice_total ELSE 0 END) AS hv_rev,
  SUM(invoice_total) AS total_rev,
  ROUND(100.0 * SUM(CASE WHEN grp='HighVol' THEN invoice_total ELSE 0 END) / SUM(invoice_total), 2) AS hv_rev_share_pct,
  SUM(CASE WHEN grp='HighVol' THEN gross_profit ELSE 0 END) AS hv_gp,
  SUM(gross_profit) AS total_gp,
  ROUND(100.0 * SUM(CASE WHEN grp='HighVol' THEN gross_profit ELSE 0 END) / NULLIF(SUM(gross_profit),0), 2) AS hv_gp_share_pct
FROM monthly_seg m
GROUP BY m.revenue_month_start
HAVING revenue_month_start >= '2023-01-01'
ORDER BY m.revenue_month_start