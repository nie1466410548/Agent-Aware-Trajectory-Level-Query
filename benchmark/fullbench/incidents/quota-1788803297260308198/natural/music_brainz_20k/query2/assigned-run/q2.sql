SELECT store, SUM(revenue_usd) AS total_revenue_usd, SUM(units_sold) AS total_units, COUNT(*) AS num_sales
FROM sales
WHERE track_id = 4122
GROUP BY store
ORDER BY total_revenue_usd DESC;
