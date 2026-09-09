SELECT 
  u."Age group",
  ROUND(AVG(t."Tag Type Count"),1) as avg_tag_types,
  ROUND(AVG(t."Personalization Tag Count"),1) as avg_personalization_tags
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"