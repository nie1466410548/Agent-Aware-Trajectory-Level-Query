SELECT track_id, store, country, units_sold, revenue_usd
FROM sales
WHERE track_id IN (4628, 14080)
ORDER BY track_id, revenue_usd DESC;
