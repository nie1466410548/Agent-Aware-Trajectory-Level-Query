SELECT customer_id,
  ROUND((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2, 2) AS risk_score,
  payment_rate_percentage, outstanding_balance, credit_score, business_stability_score, overdue_count_12m, avg_payment_days_12m
FROM quickbooks__customer_analytics
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
ORDER BY risk_score DESC