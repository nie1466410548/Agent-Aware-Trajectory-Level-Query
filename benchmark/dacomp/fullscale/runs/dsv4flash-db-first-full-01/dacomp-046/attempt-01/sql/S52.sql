SELECT 
  u."Age group",
  n."VPN Enabled",
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN network_environment_information n ON u."User ID"=n."User ID"
GROUP BY u."Age group", n."VPN Enabled"
ORDER BY u."Age group", n."VPN Enabled"