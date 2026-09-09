SELECT user_id, COUNT(DISTINCT categories_department) as dept_cnt
FROM (
  SELECT owner_user_id as user_id, categories_department FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
  UNION ALL
  SELECT creator_user_id as user_id, categories_department FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
)
GROUP BY user_id
HAVING dept_cnt > 1
LIMIT 10