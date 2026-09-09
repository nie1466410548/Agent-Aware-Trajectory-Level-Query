-- Map each requisition to a department and count open + on-hold
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
),
hm_dept AS (
  SELECT user_id, categories_department FROM ranked WHERE rn = 1
)
SELECT COALESCE(hd.categories_department, 'Unmapped') as department,
       COUNT(*) as pending_roles,
       SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END) as open_cnt,
       SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END) as onhold_cnt
FROM lever__requisition_enhanced r
LEFT JOIN hm_dept hd ON r.hiring_manager_user_id = hd.user_id
WHERE r.status IN ('open', 'on-hold')
GROUP BY COALESCE(hd.categories_department, 'Unmapped')
ORDER BY department