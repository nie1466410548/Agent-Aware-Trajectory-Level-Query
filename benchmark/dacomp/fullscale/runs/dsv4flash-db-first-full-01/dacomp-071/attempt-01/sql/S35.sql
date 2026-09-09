
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, job_title, application_sources
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment', 'Final Interview')
