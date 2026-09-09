
SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(*) AS account_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
