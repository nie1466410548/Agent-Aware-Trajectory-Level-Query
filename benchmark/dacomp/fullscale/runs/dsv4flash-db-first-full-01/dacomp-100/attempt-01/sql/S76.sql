SELECT 
  substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16), '|')-1) AS expansion_signal,
  substr(all_company_tags, instr(all_company_tags, 'sentiment_trend=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'sentiment_trend=')+16), '|')-1) AS sentiment_trend,
  COUNT(*) AS n
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%expansion_signal=%'
GROUP BY 1, 2
ORDER BY 1, 2