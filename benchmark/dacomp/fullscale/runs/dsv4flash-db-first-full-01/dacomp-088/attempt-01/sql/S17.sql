SELECT billing_state, annual_revenue
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
ORDER BY billing_state