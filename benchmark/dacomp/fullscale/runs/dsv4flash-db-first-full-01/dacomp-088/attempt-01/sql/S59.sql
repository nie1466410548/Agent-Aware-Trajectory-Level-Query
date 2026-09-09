-- New Business won opportunities per account billing state
SELECT a.billing_state AS state, COUNT(DISTINCT a.account_id) AS n_new_cust
FROM salesforce__account_daily_history a
JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
WHERE o.is_won = 1 AND o.type = 'New Business' AND a.billing_state IS NOT NULL
GROUP BY a.billing_state
ORDER BY n_new_cust DESC