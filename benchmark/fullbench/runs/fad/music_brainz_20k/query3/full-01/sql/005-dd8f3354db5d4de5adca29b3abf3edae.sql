SELECT track_id, SUM(revenue_usd) AS total_revenue_usd, SUM(units_sold) AS total_units
FROM sales
GROUP BY track_id;

