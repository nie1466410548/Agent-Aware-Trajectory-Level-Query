-- New Business won opportunities per owner state
SELECT opportunity_owner_state AS state, COUNT(DISTINCT account_id) AS n_new_cust
FROM salesforce__opportunity_enhanced
WHERE is_won = 1 AND type = 'New Business' AND opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state
ORDER BY n_new_cust DESC