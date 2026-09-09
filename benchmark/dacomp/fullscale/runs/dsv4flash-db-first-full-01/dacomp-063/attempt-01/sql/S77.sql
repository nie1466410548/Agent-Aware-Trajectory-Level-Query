-- Final profile: the extreme contradictory cohort (health>75, critical/high risk, high complexity, immediate executive review)
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN risk_category='Critical Risk' THEN 1 ELSE 0 END) as critical_cnt,
  SUM(CASE WHEN trajectory_status IN ('Declining','Deteriorating','At Risk','Volatile') THEN 1 ELSE 0 END) as adverse_trajectory,
  SUM(CASE WHEN value_delivery_percentage < 60 THEN 1 ELSE 0 END) as low_value_delivery,
  SUM(CASE WHEN success_probability < 0.4 THEN 1 ELSE 0 END) as low_success,
  SUM(CASE WHEN resolution_velocity_change_percent < 0 THEN 1 ELSE 0 END) as negative_velocity,
  SUM(CASE WHEN net_issue_growth_30d > 0 THEN 1 ELSE 0 END) as growing_backlog,
  AVG(overall_health_score) as avg_health,
  AVG(total_risk_score) as avg_total_risk,
  AVG(complexity_risk_score) as avg_complexity,
  AVG(value_delivery_percentage) as avg_delivery,
  AVG(success_probability) as avg_success_prob
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
  AND recommended_intervention = 'Immediate Executive Review Required'