-- Profile high-risk tier customers: financial contribution
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol, PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10 WHEN 'Good' THEN 35 WHEN 'Average' THEN 65 WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10 WHEN 'Loyal Customers' THEN 25 WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50 WHEN 'Need Attention' THEN 75 WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
),
risk_rated AS (
  SELECT 
    customer_id,
    CASE 
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70 THEN 'High Risk'
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 45 THEN 'Medium Risk'
      ELSE 'Low Risk'
    END AS risk_tier,
    (0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score) AS composite_risk
  FROM scored
)
SELECT 
  r.risk_tier,
  COUNT(DISTINCT r.customer_id) AS n_customers,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.gross_profit) AS total_gross_profit,
  ROUND(100.0 * SUM(p.outstanding_balance) / NULLIF((SELECT SUM(outstanding_balance) FROM quickbooks__profitability_analysis), 0), 2) AS outstanding_share_pct
FROM risk_rated r
JOIN quickbooks__profitability_analysis p ON r.customer_id = p.customer_id
GROUP BY r.risk_tier
ORDER BY r.risk_tier