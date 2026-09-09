WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 'HighRetention' 
            WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 'LowRetention'
            ELSE 'Normal' END AS anomaly_dir,
       COUNT(*) AS n,
       ROUND(AVG(c.retention_probability), 3) AS avg_ret,
       ROUND(AVG(c.transaction_value_volatility), 3) AS avg_volatility,
       ROUND(AVG(c.total_revenue), 1) AS avg_rev,
       ROUND(AVG(c.comprehensive_customer_score), 1) AS avg_score,
       ROUND(AVG(c.transaction_count), 1) AS avg_tx,
       ROUND(AVG(c.avg_transactions_per_month), 2) AS avg_tx_month,
       ROUND(AVG((c.q1_transactions+c.q2_transactions+c.q3_transactions+c.q4_transactions)*1.0/NULLIF(c.transaction_count,0)), 3) AS avg_q_total_tx_ratio,
       ROUND(AVG(CASE WHEN c.q4_transactions >= c.q1_transactions AND c.q4_transactions >= c.q2_transactions AND c.q4_transactions >= c.q3_transactions THEN 1 ELSE 0 END), 3) AS q4_dominant_share
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment, anomaly_dir
ORDER BY c.profitability_segment, anomaly_dir