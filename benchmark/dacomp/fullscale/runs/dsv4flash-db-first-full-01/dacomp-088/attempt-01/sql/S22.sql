SELECT owner_id, billing_state, COUNT(*) AS cnt
FROM salesforce__account_daily_history
WHERE billing_state IS NOT NULL
GROUP BY owner_id, billing_state
ORDER BY owner_id, cnt DESC