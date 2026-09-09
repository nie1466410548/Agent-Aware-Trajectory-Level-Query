SELECT profitability_segment, COUNT(*) as cnt, 
       AVG(retention_probability) as avg_retention, 
       AVG(total_revenue) as avg_revenue,
       AVG(comprehensive_customer_score) as avg_score,
       AVG(transaction_count) as avg_tx_count,
       AVG(avg_transactions_per_month) as avg_tx_month
FROM netsuite2_customer_analytics
GROUP BY profitability_segment
ORDER BY cnt DESC