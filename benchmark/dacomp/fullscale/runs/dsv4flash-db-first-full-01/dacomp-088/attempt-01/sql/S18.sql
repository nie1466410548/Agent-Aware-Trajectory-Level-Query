SELECT DISTINCT owner_id, billing_state
FROM salesforce__account_daily_history
WHERE billing_state IS NOT NULL
ORDER BY owner_id