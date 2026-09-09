SELECT billing_state, COUNT(DISTINCT account_id) AS n_customers, COUNT(DISTINCT owner_id) AS n_owners
FROM salesforce__account_daily_history
WHERE type = 'Customer'
GROUP BY billing_state
ORDER BY n_customers DESC