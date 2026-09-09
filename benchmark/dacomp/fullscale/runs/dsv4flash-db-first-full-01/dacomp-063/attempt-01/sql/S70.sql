-- Strategic priority recommendations
SELECT strategic_priority_recommendation, COUNT(*) as cnt
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
GROUP BY strategic_priority_recommendation
ORDER BY cnt DESC