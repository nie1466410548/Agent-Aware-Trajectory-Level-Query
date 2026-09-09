SELECT 'conversion_funnel' AS tbl, COUNT(*) AS n FROM customer360__conversion_funnel_analysis
UNION ALL SELECT 'activity_metrics', COUNT(*) FROM customer360__customer_activity_metrics
UNION ALL SELECT 'value_analysis', COUNT(*) FROM customer360__customer_value_analysis