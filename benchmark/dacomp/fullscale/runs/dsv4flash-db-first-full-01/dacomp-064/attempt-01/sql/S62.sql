-- Response patterns and breadth distribution in target cohort
SELECT response_pattern_type,
  COUNT(*) AS n,
  SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END) AS n_breadth40,
  ROUND(100.0*SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_breadth40,
  ROUND(AVG(engagement_breadth_score),1) AS avg_breadth
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY response_pattern_type
ORDER BY pct_breadth40 DESC