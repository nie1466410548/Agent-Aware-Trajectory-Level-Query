SELECT 
  u."Age group",
  t."Activity Tag",
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Activity Tag"
ORDER BY u."Age group", t."Activity Tag"