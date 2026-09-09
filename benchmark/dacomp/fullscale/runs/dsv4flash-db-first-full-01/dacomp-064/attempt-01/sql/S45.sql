-- Full profile for NON-target group (aggregated for comparison)
SELECT 
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(issues_assigned),2) AS avg_assigned,
  ROUND(AVG(issues_reported),2) AS avg_reported,
  ROUND(AVG(total_outbound_influence),2) AS avg_out,
  ROUND(AVG(total_inbound_influence),2) AS avg_in,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(strategic_value_score),2) AS avg_strat,
  ROUND(AVG(total_engagement_score),2) AS avg_total
FROM jira__stakeholder_engagement_insights
WHERE NOT (engagement_impact_score >= 3 AND cross_functional_projects >= 3)