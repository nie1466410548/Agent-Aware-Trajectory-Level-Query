-- Number of new customers per state (accounts with type='Customer')
SELECT billing_state, COUNT(DISTINCT account_id) AS n_customers
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
GROUP BY billing_state
ORDER BY n_customers DESC