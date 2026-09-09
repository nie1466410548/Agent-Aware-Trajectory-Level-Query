SELECT 
  CASE 
    WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption'
    WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption'
    ELSE 'high_sprint_adoption'
  END AS sprint_bucket,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(sprint_adoption_rate),2) AS avg_sprint,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk
FROM jira__project_risk_assessment
GROUP BY sprint_bucket
ORDER BY sprint_bucket