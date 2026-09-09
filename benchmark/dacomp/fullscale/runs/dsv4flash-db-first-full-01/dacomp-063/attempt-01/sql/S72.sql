-- Detailed breakdown of the 6 "Critical Priority - Investigate Contradictions" projects
SELECT project_id, project_key, project_name, overall_health_score, total_risk_score, complexity_risk_score, trajectory_status, value_delivery_percentage, success_probability, resolution_velocity_change_percent, net_issue_growth_30d, primary_risk_driver
FROM jira__project_risk_assessment
WHERE strategic_priority_recommendation = 'Critical Priority - Investigate Contradictions'
ORDER BY overall_health_score DESC