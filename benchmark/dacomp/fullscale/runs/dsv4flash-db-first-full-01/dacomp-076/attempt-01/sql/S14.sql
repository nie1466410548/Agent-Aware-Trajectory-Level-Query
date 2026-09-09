SELECT customer_id, COUNT(*) AS cnt
FROM netsuite2_customer_analytics
GROUP BY customer_id
HAVING cnt > 1
ORDER BY cnt DESC