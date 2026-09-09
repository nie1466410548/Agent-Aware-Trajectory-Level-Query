-- Business stability score, active months, revenue growth by segment
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
  COUNT(*) AS n,
  AVG(a.business_stability_score) AS avg_stability,
  AVG(a.active_months_last_12) AS avg_active_months,
  AVG(a.revenue_growth_rate_12m) AS avg_growth12,
  AVG(a.revenue_trend_correlation) AS avg_trend_corr,
  AVG(a.revenue_volatility) AS avg_rev_vol,
  AVG(a.days_since_last_invoice) AS avg_days_since_last
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment