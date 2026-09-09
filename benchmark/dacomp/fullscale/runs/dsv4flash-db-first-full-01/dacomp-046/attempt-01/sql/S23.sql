SELECT "Browsing Preference Tag", COUNT(*) as cnt
FROM user_tags_table t JOIN user_basic_information_table_1 u ON t."User ID"=u."User ID"
WHERE u."Age group"='<25'
GROUP BY "Browsing Preference Tag"