-- All 15 projects with health>75 and "Investigate Contradictions"
SELECT project_id, project_key, overall_health_score, total_risk_score, complexity_risk_score, risk_category, trajectory_status, value_delivery_percentage, success_probability, resolution_velocity_change_percent, net_issue_growth_30d, primary_risk_driver, recommended_intervention
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND strategic_priority_recommendation = 'Critical Priority - Investigate Contradictions'
ORDER BY overall_health_score DESC