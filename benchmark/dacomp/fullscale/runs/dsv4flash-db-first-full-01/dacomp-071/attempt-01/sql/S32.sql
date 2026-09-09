SELECT stage, job_team, COUNT(*) as cnt, ROUND(AVG(days_in_stage),1) as avg_days
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment','Final Interview')
GROUP BY stage, job_team
ORDER BY stage, cnt DESC