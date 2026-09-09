SELECT billing_state, industry, COUNT(*) AS n_customers
FROM salesforce__account_daily_history
WHERE type = 'Customer'
GROUP BY billing_state, industry
ORDER BY billing_state, n_customers DESC