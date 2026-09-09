
SELECT u.Department AS dept,
  AVG(ua."Password Attempt Count") AS avg_pw_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked,
  COUNT(*) AS acct_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
