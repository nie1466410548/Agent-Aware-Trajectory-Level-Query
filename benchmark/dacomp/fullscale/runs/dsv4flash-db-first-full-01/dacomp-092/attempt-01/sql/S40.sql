SELECT 
  COUNT(*) AS total,
  COUNT(revenue_trend_correlation) AS n_trend_corr,
  COUNT(credit_score) AS n_credit,
  COUNT(avg_payment_days_12m) AS n_pay_days,
  COUNT(overdue_count_12m) AS n_overdue,
  COUNT(overall_customer_score) AS n_overall,
  COUNT(revenue_volatility) AS n_rev_vol,
  COUNT(rfm_segment) AS n_rfm,
  COUNT(payment_behavior) AS n_payment,
  COUNT(lifecycle_stage) AS n_lifecycle,
  COUNT(customer_value_segment) AS n_value_seg,
  COUNT(risk_assessment) AS n_risk,
  COUNT(credit_grade) AS n_credit_grade,
  COUNT(payment_timeliness_score) AS n_pay_timeliness,
  COUNT(business_stability_score) AS n_biz_stab
FROM quickbooks__customer_analytics