-- Comprehensive analysis of false prosperity projects
WITH health_groups AS (
  SELECT 
    CASE WHEN overall_health_score > 75 THEN 'High Health' ELSE 'Low Health' END as health_group,
    CASE WHEN risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'High Risk Cluster' ELSE 'Normal Risk' END as risk_cluster,
    COUNT(*) as cnt,
    AVG(overall_health_score) as avg_health,
    AVG(total_risk_score) as avg_total_risk,
    AVG(complexity_risk_score) as avg_complexity,
    AVG(value_delivery_percentage) as avg_delivery_pct,
    AVG(team_stability_percentage) as avg_stability,
    AVG(success_probability) as avg_success_prob,
    AVG(resolution_velocity_change_percent) as avg_vel_change,
    AVG(health_risk_score) as avg_health_risk,
    AVG(schedule_risk_score) as avg_schedule_risk,
    AVG(resource_risk_score) as avg_resource_risk
  FROM jira__project_risk_assessment
  GROUP BY health_group, risk_cluster
)
SELECT * FROM health_groups ORDER BY health_group, risk_cluster