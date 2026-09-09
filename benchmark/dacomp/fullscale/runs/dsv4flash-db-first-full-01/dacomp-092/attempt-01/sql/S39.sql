-- Revenue trend correlation and other continuous behavioral features by segment
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
  AVG(a.revenue_trend_correlation) AS avg_trend_corr,
  AVG(a.credit_score) AS avg_credit_score,
  AVG(a.avg_payment_days_12m) AS avg_payment_days,
  AVG(a.overdue_count_12m) AS avg_overdue_count,
  AVG(a.overall_customer_score) AS avg_overall_score,
  AVG(a.revenue_volatility) AS avg_rev_volatility
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment