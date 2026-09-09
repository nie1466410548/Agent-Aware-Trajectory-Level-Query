WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       COUNT(*) AS n_rows,
       SUM(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) AS anomaly_rows,
       SUM(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) AS high_anomaly,
       SUM(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 1 ELSE 0 END) AS low_anomaly,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END), 3) AS anomaly_volatility,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) <= 0.15 THEN c.transaction_value_volatility END), 3) AS normal_volatility,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END), 1) AS anomaly_score,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END), 1) AS anomaly_revenue
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment
ORDER BY anomaly_rows DESC