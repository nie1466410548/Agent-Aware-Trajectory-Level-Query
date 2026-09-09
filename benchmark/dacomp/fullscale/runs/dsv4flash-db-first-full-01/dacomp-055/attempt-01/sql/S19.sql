SELECT m.marketo_lead_id, COUNT(DISTINCT c.customer360_id) AS distinct_ids, COUNT(*) AS cnt, COUNT(DISTINCT c.total_sales_amount) AS distinct_sales
FROM customer360__customer c
JOIN customer360__mapping m ON c.customer360_id = m.customer360_id
WHERE m.marketo_lead_id = 8915
GROUP BY m.marketo_lead_id