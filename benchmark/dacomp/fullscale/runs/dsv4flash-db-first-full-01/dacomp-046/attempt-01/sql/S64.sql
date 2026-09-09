
SELECT u."Age group" as age, 
  t."Is High-Value User" as hv,
  t."Is Potential Conversion User" as pc,
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User", t."Is Potential Conversion User"
