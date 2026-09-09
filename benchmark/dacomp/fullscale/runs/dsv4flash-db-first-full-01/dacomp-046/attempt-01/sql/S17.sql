SELECT 
  u."Age group",
  t."Price Sensitivity",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"
ORDER BY u."Age group", t."Price Sensitivity"