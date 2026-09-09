WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention,
           COUNT(*) AS seg_count
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.customer_id, c.customer_name, c.profitability_segment, 
       c.retention_probability, s.avg_retention,
       c.retention_probability - s.avg_retention AS deviation,
       c.total_revenue, c.transaction_count, c.avg_transactions_per_month,
       c.comprehensive_customer_score, c.transaction_value_volatility,
       c.lifecycle_stage, c.value_tier, c.seasonal_preference,
       c.transaction_consistency, c.activity_status, c.engagement_frequency,
       c.q1_transactions, c.q2_transactions, c.q3_transactions, c.q4_transactions,
       c.customer_age_days, c.growth_potential
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
WHERE ABS(c.retention_probability - s.avg_retention) > 0.15
ORDER BY ABS(c.retention_probability - s.avg_retention) DESC