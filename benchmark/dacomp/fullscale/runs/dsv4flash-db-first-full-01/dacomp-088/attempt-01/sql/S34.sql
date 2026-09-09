-- Per-state opportunity stats (owner state)
SELECT opportunity_owner_state AS state,
       COUNT(*) AS n_opps,
       SUM(is_won) AS won_opps,
       ROUND(AVG(CASE WHEN is_won=1 THEN amount END),2) AS avg_won_amount,
       ROUND(AVG(CASE WHEN is_won=1 THEN probability END),2) AS avg_won_prob,
       ROUND(AVG(CASE WHEN is_won=1 THEN days_to_close END),2) AS avg_won_cycle_days,
       ROUND(AVG(probability),2) AS avg_probability,
       ROUND(AVG(days_to_close),2) AS avg_cycle_days
FROM salesforce__opportunity_enhanced
WHERE opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state