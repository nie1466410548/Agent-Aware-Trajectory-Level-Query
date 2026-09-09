-- Recommended strategies for target cohort
SELECT recommended_engagement_strategy, COUNT(*) n,
  ROUND(AVG(engagement_depth_score),2) avg_depth,
  ROUND(AVG(engagement_breadth_score),2) avg_breadth
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY recommended_engagement_strategy
ORDER BY n DESC