SELECT company_name, COUNT(DISTINCT renewal_window) AS n_windows, GROUP_CONCAT(DISTINCT renewal_window) AS windows FROM (
  SELECT company_id, company_name, CASE 
    WHEN instr(all_company_tags, 'renewal_window=') > 0 THEN 
      substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15, 
        CASE WHEN instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15), '|') > 0 
             THEN instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15), '|') - 1
             ELSE 100 END)
    ELSE NULL END AS renewal_window
  FROM intercom__company_enhanced
) GROUP BY company_name HAVING n_windows > 1 LIMIT 5