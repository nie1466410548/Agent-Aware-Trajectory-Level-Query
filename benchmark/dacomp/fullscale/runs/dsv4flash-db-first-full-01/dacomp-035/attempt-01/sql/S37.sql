SELECT 
  u.Department,
  nc."VPN Status",
  nc."Proxy Status",
  nc."Firewall Status",
  COUNT(*) AS cnt
FROM network_connections_table nc
JOIN login_records_table l ON nc."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, nc."VPN Status", nc."Proxy Status", nc."Firewall Status"
ORDER BY u.Department, cnt DESC