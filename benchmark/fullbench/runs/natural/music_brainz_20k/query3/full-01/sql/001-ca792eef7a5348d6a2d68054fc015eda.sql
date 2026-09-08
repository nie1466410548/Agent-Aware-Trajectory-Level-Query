SELECT track_id, SUM(revenue_usd) AS total_revenue FROM sales GROUP BY track_id ORDER BY total_revenue DESC LIMIT 20
