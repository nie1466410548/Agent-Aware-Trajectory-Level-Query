
    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state
