SELECT annual_revenue AS revenue, COUNT(*) AS cnt
FROM salesforce__customer_360_view
WHERE annual_revenue IS NOT NULL
GROUP BY annual_revenue
ORDER BY revenue DESC
LIMIT 20