-- At-risk high-impact stakeholders: development opportunities
SELECT development_opportunity, COUNT(*) AS n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score = 5 AND engagement_risk_status IN ('At Risk','Disengaged')
  AND cross_functional_projects >= 3
GROUP BY development_opportunity
ORDER BY n DESC