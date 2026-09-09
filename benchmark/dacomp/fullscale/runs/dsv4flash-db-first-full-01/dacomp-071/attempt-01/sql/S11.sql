
SELECT stage_id, stage, archive_reason, COUNT(*) as cnt
FROM lever__opportunity_stage_history
GROUP BY stage_id, stage, archive_reason
ORDER BY stage_id, cnt DESC
