SELECT 
  CASE 
    WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)'
    WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)'
    WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)'
    ELSE 'very_high_complexity_(>75)'
  END AS comp_bucket,
  COUNT(*) AS n,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(overall_health_score),2) AS avg_health,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk,
  ROUND(AVG(team_stability_percentage),2) AS avg_team_stability
FROM jira__project_risk_assessment
GROUP BY comp_bucket
ORDER BY comp_bucket