SELECT customer_id, customer_name, profitability_segment, retention_probability, total_revenue, transaction_count, comprehensive_customer_score, lifecycle_stage, value_tier, seasonal_preference, transaction_consistency, customer_analytics_id
FROM netsuite2_customer_analytics
WHERE customer_id = 'NET01146543590'
ORDER BY retention_probability