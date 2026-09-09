-- Development opportunities distribution for target cohort
SELECT development_opportunity, COUNT(*) n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY development_opportunity
ORDER BY n DESC
LIMIT 20