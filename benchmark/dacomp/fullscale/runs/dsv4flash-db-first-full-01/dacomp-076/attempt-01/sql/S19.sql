WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT customer_id) AS unique_customers,
       COUNT(*) FILTER (WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_rows,
       COUNT(DISTINCT c.customer_id) FILTER (WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_customers
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment