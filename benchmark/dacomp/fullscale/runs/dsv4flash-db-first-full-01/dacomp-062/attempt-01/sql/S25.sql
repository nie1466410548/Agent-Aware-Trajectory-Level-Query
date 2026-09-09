SELECT 
  SUM(total_projects_involved) AS total_involvements,
  SUM(cross_functional_projects) AS total_cross_func,
  COUNT(*) AS n_stakeholders,
  COUNT(DISTINCT total_projects_involved) AS distinct_project_counts
FROM jira__stakeholder_engagement_insights