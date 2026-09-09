-- Map requisition hiring managers to departments via posting user IDs
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
)
SELECT categories_department, COUNT(DISTINCT user_id) as mapped_hms
FROM ranked
WHERE rn = 1
GROUP BY categories_department
ORDER BY categories_department