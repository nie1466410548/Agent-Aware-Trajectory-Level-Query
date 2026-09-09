SELECT COUNT(*) AS total, SUM(CASE WHEN parent_task_id IS NOT NULL AND parent_task_id != task_id THEN 1 ELSE 0 END) AS has_parent,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed
FROM asana__task_lifecycle_analysis WHERE is_valid_record=1