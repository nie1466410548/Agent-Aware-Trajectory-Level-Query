-- Overview of account types and won opp relationships
SELECT a.type,
       COUNT(DISTINCT a.account_id) AS n_accounts,
       COUNT(DISTINCT CASE WHEN o.is_won = 1 THEN a.account_id END) AS n_with_won
FROM salesforce__account_daily_history a
LEFT JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
GROUP BY a.type
ORDER BY n_accounts DESC