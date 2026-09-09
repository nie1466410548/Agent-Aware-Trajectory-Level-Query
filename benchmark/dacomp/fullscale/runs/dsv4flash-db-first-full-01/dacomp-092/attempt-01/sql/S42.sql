SELECT 
  COUNT(*) AS total,
  COUNT(customer_value_segment) AS n_value_seg,
  COUNT(business_stability_score) AS n_biz_stab,
  COUNT(activity_status) AS n_activity,
  COUNT(customer_maturity_stage) AS n_maturity,
  COUNT(revenue_growth_rate_12m) AS n_growth12,
  COUNT(active_months_last_12) AS n_act_months,
  COUNT(payment_rate_percentage) AS n_pay_rate,
  COUNT(data_quality_flag) AS n_dq,
  COUNT(recommended_action) AS n_recommended
FROM quickbooks__customer_analytics