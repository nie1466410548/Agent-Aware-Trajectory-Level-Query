SELECT track_id,
       SUM(revenue_usd) AS total_revenue_usd,
       SUM(units_sold) AS total_units,
       COUNT(*) AS sale_count
FROM sales
GROUP BY track_id
ORDER BY total_revenue_usd DESC
LIMIT 20;

