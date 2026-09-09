SELECT COUNT(*) AS unmatched, COUNT(DISTINCT assignee_user_id) AS uniq_unmatched
FROM asana__task_lifecycle_analysis t LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.user_id IS NULL