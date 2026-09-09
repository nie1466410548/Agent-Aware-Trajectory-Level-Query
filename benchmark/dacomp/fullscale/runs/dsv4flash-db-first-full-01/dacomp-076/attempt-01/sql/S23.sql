WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END),1) AS high_ret_avg_rev,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.total_revenue END),1) AS low_ret_avg_rev,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_count END),2) AS high_ret_avg_tx,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_count END),2) AS low_ret_avg_tx,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END),1) AS high_ret_avg_score,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.comprehensive_customer_score END),1) AS low_ret_avg_score,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END),3) AS high_ret_avg_vol,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_value_volatility END),3) AS low_ret_avg_vol
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment