-- Monthly workload trend for target stakeholders (assignee side)
SELECT 
  strftime('%Y-%m', i.created_at) AS month,
  COUNT(*) AS n_created,
  ROUND(AVG(i.open_duration_seconds/86400.0),2) AS avg_open_days,
  ROUND(AVG(i.any_assignment_duration_seconds/86400.0),2) AS avg_assignment_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio,
  COUNT(DISTINCT i.assignee_user_id) AS n_distinct_assignees
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY strftime('%Y-%m', i.created_at)
ORDER BY month