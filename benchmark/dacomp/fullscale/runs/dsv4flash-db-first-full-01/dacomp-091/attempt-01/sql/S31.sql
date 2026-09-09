
  SELECT vendor_id, vendor_display_name, annual_spend_growth_pct, overall_performance_score,
         spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score,
         avg_monthly_spend
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
