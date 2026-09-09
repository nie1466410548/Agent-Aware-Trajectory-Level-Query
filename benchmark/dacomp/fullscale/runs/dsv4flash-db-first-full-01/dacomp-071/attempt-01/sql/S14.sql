
SELECT opportunity_id, stage_id, stage, valid_from, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from
