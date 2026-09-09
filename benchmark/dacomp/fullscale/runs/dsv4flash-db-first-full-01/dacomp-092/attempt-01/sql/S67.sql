-- High-risk tier profile details
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
    v.vol,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10 WHEN 'Good' THEN 35 WHEN 'Average' THEN 65 WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10 WHEN 'Loyal Customers' THEN 25 WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50 WHEN 'Need Attention' THEN 75 WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score,
    a.payment_behavior, a.rfm_segment, a.business_stability_score, a.revenue_trend_correlation,
    a.active_months_last_12, a.revenue_growth_rate_12m
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
)
SELECT 
  COUNT(*) AS n_high_risk,
  SUM(CASE WHEN payment_behavior = 'Poor' THEN 1 ELSE 0 END) AS n_poor_payment,
  SUM(CASE WHEN rfm_segment = 'At Risk' THEN 1 ELSE 0 END) AS n_at_risk,
  SUM(CASE WHEN revenue_trend_correlation < 0 THEN 1 ELSE 0 END) AS n_negative_trend,
  ROUND(AVG(business_stability_score), 1) AS avg_stability,
  ROUND(AVG(active_months_last_12), 1) AS avg_active_months,
  ROUND(AVG(revenue_growth_rate_12m), 2) AS avg_growth_12m,
  ROUND(AVG(vol), 3) AS avg_margin_vol
FROM scored
WHERE 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70