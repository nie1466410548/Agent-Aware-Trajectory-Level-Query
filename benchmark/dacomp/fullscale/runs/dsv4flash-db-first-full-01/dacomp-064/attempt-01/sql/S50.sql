
SELECT *, 
  CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END AS is_target
FROM jira__stakeholder_engagement_insights
