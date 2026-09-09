SELECT vendor_id, vendor_name, vendor_company_name, vendor_display_name, total_lifetime_spend, annual_spend_growth_pct, overall_performance_score, spend_volatility, payment_completion_rate, business_value_score
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
ORDER BY annual_spend_growth_pct