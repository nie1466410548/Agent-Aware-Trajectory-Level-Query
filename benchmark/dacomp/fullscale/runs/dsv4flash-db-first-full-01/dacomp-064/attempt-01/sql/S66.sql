-- At-risk high-impact stakeholders: recommended strategies
SELECT recommended_engagement_strategy, COUNT(*) AS n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score = 5 AND engagement_risk_status IN ('At Risk','Disengaged')
  AND cross_functional_projects >= 3
GROUP BY recommended_engagement_strategy
ORDER BY n DESC