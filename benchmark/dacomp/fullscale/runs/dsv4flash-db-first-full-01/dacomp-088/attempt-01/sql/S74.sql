
    SELECT opportunity_owner_state AS state,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(probability) AS avg_probability,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle,
           SUM(is_won)*1.0/COUNT(*) AS win_rate
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IN ('New York','California','Oregon')
    GROUP BY opportunity_owner_state