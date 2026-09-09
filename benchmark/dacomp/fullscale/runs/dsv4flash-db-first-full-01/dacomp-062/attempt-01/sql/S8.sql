SELECT 
  MIN(direct_network_connections) AS min_conn,
  AVG(direct_network_connections) AS avg_conn,
  MAX(direct_network_connections) AS max_conn,
  MEDIAN(direct_network_connections) AS median_conn,
  STDEV(direct_network_connections) AS std_conn
FROM jira__stakeholder_engagement_insights