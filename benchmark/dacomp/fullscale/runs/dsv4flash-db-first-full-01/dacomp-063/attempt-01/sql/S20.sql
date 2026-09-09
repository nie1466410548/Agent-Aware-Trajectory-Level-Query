SELECT project_id, project_key, project_name, overall_health_score, complexity_risk_score, total_risk_score, risk_category, primary_risk_factor, recommended_intervention, trajectory_status
FROM jira__project_risk_assessment 
WHERE overall_health_score > 75
ORDER BY overall_health_score DESC
LIMIT 20