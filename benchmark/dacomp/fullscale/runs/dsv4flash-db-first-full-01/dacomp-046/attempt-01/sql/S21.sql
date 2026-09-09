SELECT 
  u."Age group",
  t."Category Preference",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
WHERE t."Category Preference" IS NOT NULL AND t."Category Preference" != 'None'
GROUP BY u."Age group", t."Category Preference"
ORDER BY u."Age group", count DESC