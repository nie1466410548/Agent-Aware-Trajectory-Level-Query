SELECT track_id, SUM(revenue_usd) AS total_revenue, SUM(units_sold) AS total_units, COUNT(*) AS n_sales FROM sales GROUP BY track_id ORDER BY total_revenue DESC
