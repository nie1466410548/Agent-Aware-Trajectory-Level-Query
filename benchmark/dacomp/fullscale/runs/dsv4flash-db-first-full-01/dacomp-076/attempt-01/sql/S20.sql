WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.*, 
       s.avg_retention,
       c.retention_probability - s.avg_retention AS deviation,
       CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END AS is_anomaly,
       CASE WHEN c.retention_probability > s.avg_retention THEN 1 ELSE 0 END AS is_above_avg
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment