SELECT "Age group", COUNT(*) as user_count
FROM user_basic_information_table_1
GROUP BY "Age group"
ORDER BY "Age group"