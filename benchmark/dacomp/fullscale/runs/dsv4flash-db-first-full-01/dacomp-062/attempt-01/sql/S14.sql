SELECT 
  CASE 
    WHEN direct_network_connections <= 5 THEN '1_low_(<=5)'
    WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)'
    WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)'
    WHEN direct_network_connections <= 35 THEN '4_high_(21-35)'
    ELSE '5_very_high_(>35)'
  END AS conn_bucket,
  COUNT(*) AS n,
  ROUND(AVG(total_projects_involved),2) AS avg_projects,
  ROUND(AVG(cross_functional_projects),2) AS avg_cross_func,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(total_inbound_influence),2) AS avg_inbound,
  ROUND(AVG(total_outbound_influence),2) AS avg_outbound
FROM jira__stakeholder_engagement_insights
GROUP BY conn_bucket
ORDER BY conn_bucket