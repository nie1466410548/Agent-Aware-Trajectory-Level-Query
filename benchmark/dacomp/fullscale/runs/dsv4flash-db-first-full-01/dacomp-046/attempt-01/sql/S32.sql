SELECT 
  u."Age group",
  ROUND(AVG(u."Login Count"),1) as avg_login,
  ROUND(AVG(u."Device count"),2) as avg_devices,
  ROUND(100.0*SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/COUNT(*),1) as sms_sub_pct
FROM user_basic_information_table_1 u
GROUP BY u."Age group"
ORDER BY u."Age group"