-- Multi-dimensional risk scoring model: compute components per customer
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol,
    PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
fin AS (
  SELECT customer_id,
    SUM(invoice_total) AS total_invoice,
    SUM(outstanding_balance) AS total_outstanding,
    SUM(collected_amount) AS total_collected,
    COUNT(*) AS n_invoices,
    AVG(invoice_gross_margin_pct) AS avg_margin_pct
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
scored AS (
  SELECT 
    v.customer_id,
    v.vol,
    v.vol_pct_rank,
    a.payment_behavior,
    a.rfm_segment,
    a.revenue_trend_correlation,
    a.business_stability_score,
    a.active_months_last_12,
    a.revenue_growth_rate_12m,
    f.total_outstanding,
    f.total_invoice,
    f.n_invoices,
    f.avg_margin_pct,
    -- Dimension scores (each normalized 0-100)
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10
      WHEN 'Good' THEN 35
      WHEN 'Average' THEN 65
      WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10
      WHEN 'Loyal Customers' THEN 25
      WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50
      WHEN 'Need Attention' THEN 75
      WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
  JOIN fin f ON v.customer_id = f.customer_id
)
SELECT 
  customer_id, vol, vol_pct_rank, payment_behavior, rfm_segment,
  ROUND(revenue_trend_correlation, 3) AS trend_corr,
  business_stability_score, active_months_last_12,
  ROUND(total_outstanding, 2) AS total_outstanding,
  ROUND(total_invoice, 2) AS total_invoice,
  ROUND(vol_score, 1) AS vol_score,
  payment_score, rfm_score, trend_score, stability_score
FROM scored
ORDER BY vol_pct_rank DESC
LIMIT 15