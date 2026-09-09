SELECT p.categories_department, COUNT(DISTINCT p.owner_user_id) as owners, COUNT(DISTINCT p.creator_user_id) as creators
FROM lever__posting_enhanced p
GROUP BY p.categories_department
ORDER BY p.categories_department