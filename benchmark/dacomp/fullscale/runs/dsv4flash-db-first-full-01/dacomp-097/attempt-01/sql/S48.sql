SELECT 
  SUM(is_active_1d) as act_1d, SUM(is_active_7d) as act_7d, SUM(is_active_30d) as act_30d,
  SUM(retained_7d) as ret_7d, SUM(retained_30d) as ret_30d,
  COUNT(*) as total
FROM intercom__contact_enhanced