SELECT profitability_segment,
       COUNT(*) AS n_rows,
       COUNT(DISTINCT customer_id) AS n_customers,
       MIN(retention_probability) AS min_ret,
       MAX(retention_probability) AS max_ret,
       AVG(retention_probability) AS avg_ret,
       AVG(transaction_value_volatility) AS avg_volatility,
       AVG(customer_age_days) AS avg_age,
       AVG(net_profit) AS avg_net_profit
FROM netsuite2_customer_analytics
GROUP BY profitability_segment