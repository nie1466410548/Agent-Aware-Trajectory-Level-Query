SELECT opportunity_owner_state, 
       COUNT(*) AS n_opps,
       COUNT(DISTINCT account_id) AS n_accounts,
       AVG(CASE WHEN is_won = 1 THEN amount END) AS avg_won_amount,
       AVG(probability) AS avg_probability,
       AVG(days_to_close) AS avg_days_to_close,
       SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS won_opps,
       COUNT(*) AS total_opps
FROM salesforce__opportunity_enhanced
WHERE opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state
ORDER BY n_opps DESC