SELECT store, SUM(revenue_usd) AS total_revenue, COUNT(*) AS sales FROM sales WHERE track_id = 4122 GROUP BY store ORDER BY total_revenue DESC;
