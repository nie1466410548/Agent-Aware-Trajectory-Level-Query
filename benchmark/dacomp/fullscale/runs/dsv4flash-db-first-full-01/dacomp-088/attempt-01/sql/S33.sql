-- Per-state customer stats: count, mean, median revenue
SELECT billing_state AS state,
       COUNT(DISTINCT account_id) AS n_customers,
       ROUND(AVG(annual_revenue),2) AS avg_revenue,
       ROUND(SUM(annual_revenue),2) AS total_revenue
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
GROUP BY billing_state