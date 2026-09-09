SELECT stage_id, stage, MIN(days_in_stage) as min_d, MAX(days_in_stage) as max_d, ROUND(AVG(days_in_stage),2) as avg_d, COUNT(*) as n
FROM lever__opportunity_stage_history
GROUP BY stage_id, stage ORDER BY stage_id