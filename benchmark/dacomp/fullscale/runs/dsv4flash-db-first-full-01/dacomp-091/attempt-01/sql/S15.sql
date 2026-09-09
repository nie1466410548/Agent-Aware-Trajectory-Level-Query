SELECT vendor_id,
  ROUND(spend_volatility / NULLIF(total_lifetime_spend,0), 6) AS spend_vol_coef,
  ROUND(payment_completion_rate*0.4 + business_value_score/10.0*0.6, 6) AS composite_risk_score,
  annual_spend_growth_pct, overall_performance_score, total_lifetime_spend,
  ROUND(spend_current_year,2) AS spend_current_year, ROUND(spend_prev_year,2) AS spend_prev_year
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
ORDER BY composite_risk_score DESC