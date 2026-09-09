SELECT 
  COUNT(*) AS n,
  ROUND(AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS avg_risk_score,
  ROUND(MIN((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS min_risk_score,
  ROUND(MAX((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS max_risk_score,
  ROUND(AVG(payment_rate_percentage),2) AS avg_payment_rate,
  ROUND(AVG(outstanding_balance),2) AS avg_outstanding_balance,
  ROUND(SUM(outstanding_balance),2) AS total_outstanding_balance,
  ROUND(AVG(credit_score),2) AS avg_credit_score,
  ROUND(AVG(business_stability_score),2) AS avg_stability_score
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000