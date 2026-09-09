-- Join monthly high-vol share with financial dashboard
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
    SUM(CASE WHEN h.customer_id IS NOT NULL THEN p.invoice_total ELSE 0 END) AS hv_rev,
    SUM(p.invoice_total) AS total_rev,
    SUM(CASE WHEN h.customer_id IS NOT NULL THEN p.gross_profit ELSE 0 END) AS hv_gp,
    SUM(p.gross_profit) AS total_gp
  FROM quickbooks__profitability_analysis p
  LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
  GROUP BY p.revenue_month_start
)
SELECT 
  m.revenue_month_start,
  ROUND(100.0 * m.hv_rev / NULLIF(m.total_rev, 0), 2) AS hv_rev_share,
  ROUND(100.0 * m.hv_gp / NULLIF(m.total_gp, 0), 2) AS hv_gp_share,
  f.business_health_score,
  f.collection_rate_percentage,
  f.gross_margin_percentage,
  f.total_revenue,
  f.outstanding_receivables,
  f.collection_risk_level
FROM monthly_seg m
JOIN quickbooks__financial_dashboard f 
  ON STRFTIME('%Y-%m', m.revenue_month_start) = STRFTIME('%Y-%m', f.dashboard_month)
ORDER BY m.revenue_month_start