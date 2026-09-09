SELECT MIN(retention_probability) AS min_ret, MAX(retention_probability) AS max_ret,
       AVG(retention_probability) AS avg_ret, 
       COUNT(*) FILTER (WHERE retention_probability > 0.7) AS high_ret,
       COUNT(*) FILTER (WHERE retention_probability < 0.3) AS low_ret
FROM netsuite2_customer_analytics