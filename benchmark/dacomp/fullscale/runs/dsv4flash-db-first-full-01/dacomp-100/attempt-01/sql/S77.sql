SELECT 
  substr(all_company_tags, instr(all_company_tags, 'last_value_milestone=')+21,
    instr(substr(all_company_tags, instr(all_company_tags, 'last_value_milestone=')+21), '|')-1) AS milestone,
  substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16), '|')-1) AS expansion_signal,
  COUNT(*) AS n
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%expansion_signal=%'
GROUP BY 1, 2
ORDER BY 1, 2