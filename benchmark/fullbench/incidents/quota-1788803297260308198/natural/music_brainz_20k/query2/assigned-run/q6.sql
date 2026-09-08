SELECT store, SUM(revenue_usd) AS total_revenue_usd, SUM(units_sold) AS total_units
FROM sales
WHERE track_id IN (4122, 4628, 14080)
GROUP BY store
ORDER BY total_revenue_usd DESC;
