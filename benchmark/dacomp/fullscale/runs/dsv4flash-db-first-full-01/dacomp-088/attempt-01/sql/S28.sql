-- Count of won opportunities per account (to identify active customers)
SELECT a.billing_state, COUNT(DISTINCT a.account_id) AS n_customers_with_won_opps
FROM salesforce__account_daily_history a
JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
WHERE o.is_won = 1 AND a.billing_state IS NOT NULL
GROUP BY a.billing_state
ORDER BY n_customers_with_won_opps DESC