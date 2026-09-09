SELECT 
  u."Age group",
  t."Purchase Preference Tag",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
WHERE t."Purchase Preference Tag" != 'None'
GROUP BY u."Age group", t."Purchase Preference Tag"
ORDER BY u."Age group", count DESC