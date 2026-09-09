SELECT COUNT(DISTINCT project_key) AS distinct_keys,
       COUNT(DISTINCT project_name) AS distinct_names,
       COUNT(DISTINCT project_id) AS distinct_ids
FROM jira__project_risk_assessment