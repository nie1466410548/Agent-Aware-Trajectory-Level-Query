SELECT 
  SUM(CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS n_target,
  SUM(CASE WHEN engagement_impact_score >= 3 THEN 1 ELSE 0 END) AS n_high_impact,
  SUM(CASE WHEN cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS n_cross_func,
  COUNT(*) AS n_total
FROM jira__stakeholder_engagement_insights