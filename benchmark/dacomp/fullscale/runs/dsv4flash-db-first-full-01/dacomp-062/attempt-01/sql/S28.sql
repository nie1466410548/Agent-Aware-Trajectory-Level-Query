SELECT 
  CASE 
    WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)'
    WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)'
    ELSE 'high_stability_(>=75)'
  END AS stability_bucket,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(team_stability_percentage),2) AS avg_stability,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk
FROM jira__project_risk_assessment
GROUP BY stability_bucket
ORDER BY stability_bucket