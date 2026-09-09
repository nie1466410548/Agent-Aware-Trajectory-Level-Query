SELECT
  COUNT(*) AS n_vendors,
  ROUND(AVG(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS avg_spend_vol_coef,
  ROUND(MIN(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS min_spend_vol_coef,
  ROUND(MAX(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS max_spend_vol_coef,
  ROUND(AVG(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS avg_composite_risk,
  ROUND(MIN(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS min_composite_risk,
  ROUND(MAX(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS max_composite_risk,
  ROUND(SUM(total_lifetime_spend),2) AS total_lifetime_spend_sum,
  ROUND(SUM(spend_volatility),2) AS total_spend_volatility,
  ROUND(SUM(total_outstanding),2) AS total_outstanding
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7