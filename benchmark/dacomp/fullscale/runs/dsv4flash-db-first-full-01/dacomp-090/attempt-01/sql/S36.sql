
  SELECT customer_id, outstanding_balance,
    (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
