-- User demographics by membership level
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS user_count,
  ROUND(AVG(u."Login Count"),1) AS avg_login_count,
  ROUND(AVG(u."Device count"),1) AS avg_device_count,
  ROUND(SUM(CASE WHEN u."Payment enabled" = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS payment_pct,
  ROUND(SUM(CASE WHEN u."Real-name verification status" = 'Verified' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS verified_pct
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group