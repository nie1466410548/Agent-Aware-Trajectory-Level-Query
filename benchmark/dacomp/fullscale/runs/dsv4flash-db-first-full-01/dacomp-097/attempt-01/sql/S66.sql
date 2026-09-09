SELECT 
  is_active_30d, retained_30d, COUNT(*) as cnt
FROM intercom__contact_enhanced
GROUP BY is_active_30d, retained_30d
ORDER BY is_active_30d, retained_30d