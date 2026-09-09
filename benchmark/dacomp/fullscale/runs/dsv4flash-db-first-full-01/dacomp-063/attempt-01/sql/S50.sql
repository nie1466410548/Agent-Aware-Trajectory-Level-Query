-- Project metrics: False prosperity vs others
SELECT 
  CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END as group_label,
  COUNT(*) as cnt,
  ROUND(AVG(overall_health_score),2) as avg_health,
  ROUND(AVG(total_risk_score),2) as avg_total_risk,
  ROUND(AVG(health_risk_score),2) as avg_health_risk,
  ROUND(AVG(schedule_risk_score),2) as avg_schedule_risk,
  ROUND(AVG(resource_risk_score),2) as avg_resource_risk,
  ROUND(AVG(complexity_risk_score),2) as avg_complexity_risk,
  ROUND(AVG(scope_risk_score),2) as avg_scope_risk,
  ROUND(AVG(success_probability),3) as avg_success_prob,
  ROUND(AVG(value_delivery_percentage),2) as avg_delivery_pct,
  ROUND(AVG(team_stability_percentage),2) as avg_stability,
  ROUND(AVG(resolution_velocity_change_percent),2) as avg_vel_change,
  ROUND(AVG(net_issue_growth_30d),2) as avg_issue_growth,
  ROUND(AVG(high_delay_cost_issues),2) as avg_delay_issues,
  ROUND(AVG(total_hours_invested),2) as avg_hours,
  ROUND(AVG(estimated_project_value_points),2) as avg_est_value,
  ROUND(AVG(delivered_value_points),2) as avg_delivered_value,
  ROUND(AVG(sprint_adoption_rate),2) as avg_sprint_adopt
FROM jira__project_risk_assessment
GROUP BY group_label