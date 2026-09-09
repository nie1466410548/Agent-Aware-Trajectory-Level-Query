
SELECT u."Age group" as age, 
  t."Price Sensitivity" as ps, 
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"
