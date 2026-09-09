SELECT engagement_risk_status, COUNT(*) AS n,
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(total_outbound_influence),2) AS avg_out,
  ROUND(AVG(total_inbound_influence),2) AS avg_in
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY engagement_risk_status
ORDER BY n DESC