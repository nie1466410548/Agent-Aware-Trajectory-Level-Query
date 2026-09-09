SELECT 
  SUM(CASE WHEN renewal_window='inside_90_days' THEN 1 ELSE 0 END) AS inside_90,
  SUM(CASE WHEN renewal_window='within_30_days_past' THEN 1 ELSE 0 END) AS past_30,
  SUM(CASE WHEN renewal_window='future_90_plus' THEN 1 ELSE 0 END) AS future_90
FROM (
  SELECT company_id, renewal_window FROM (
    SELECT company_id, all_company_tags,
      substr(all_company_tags, instr(all_company_tags, 'renewal_window=')+15, 
        instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=')+15), '|')-1) AS renewal_window
    FROM intercom__company_enhanced
  )
)