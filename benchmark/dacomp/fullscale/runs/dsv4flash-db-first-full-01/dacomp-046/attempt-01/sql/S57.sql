
SELECT u."Age group" as age, t."Purchase Preference Tag" as pref, COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
WHERE t."Purchase Preference Tag" != 'None'
GROUP BY u."Age group", t."Purchase Preference Tag"
