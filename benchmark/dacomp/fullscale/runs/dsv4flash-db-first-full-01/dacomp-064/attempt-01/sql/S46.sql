-- Target stakeholders by response_pattern_type with full metrics
SELECT 
  response_pattern_type,
  COUNT(*) AS n_stakeholders,
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(total_outbound_influence - total_inbound_influence),2) AS avg_influence_imbalance,
  ROUND(AVG(issues_assigned*1.0/NULLIF(issues_reported,0)),2) AS avg_assign_report_ratio,
  ROUND(AVG(direct_network_connections),2) AS avg_connections,
  ROUND(AVG(strategic_value_score),2) AS avg_strategic,
  ROUND(AVG(total_engagement_score),2) AS avg_total_score,
  SUM(CASE WHEN engagement_risk_status = 'At Risk' OR engagement_risk_status = 'Disengaged' THEN 1 ELSE 0 END) AS n_at_risk
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY response_pattern_type
ORDER BY n_stakeholders DESC