SELECT stage, archive_reason, COUNT(*) as cnt
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment','Final Interview')
GROUP BY stage, archive_reason
ORDER BY stage, cnt DESC