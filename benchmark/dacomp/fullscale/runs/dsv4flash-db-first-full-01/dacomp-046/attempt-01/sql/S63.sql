
SELECT u."Age group" as age, 
  t."Spending Power" as sp, 
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Spending Power"
