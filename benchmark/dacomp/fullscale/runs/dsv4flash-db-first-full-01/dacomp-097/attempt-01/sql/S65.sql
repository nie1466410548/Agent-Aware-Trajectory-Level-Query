-- Check relationship between is_active and retained per contact
SELECT 
  is_active_7d, retained_7d, COUNT(*) as cnt
FROM intercom__contact_enhanced
GROUP BY is_active_7d, retained_7d
ORDER BY is_active_7d, retained_7d