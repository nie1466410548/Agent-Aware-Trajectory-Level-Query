SELECT 
  u.Department,
  COUNT(*) AS total_connections,
  SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) AS no_vpn,
  SUM(CASE WHEN nc."Proxy Status" = 'Closed' THEN 1 ELSE 0 END) AS proxy_closed,
  SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) AS firewall_closed,
  ROUND(100.0 * SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_no_vpn,
  ROUND(100.0 * SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_firewall_closed
FROM network_connections_table nc
JOIN login_records_table l ON nc."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_no_vpn DESC