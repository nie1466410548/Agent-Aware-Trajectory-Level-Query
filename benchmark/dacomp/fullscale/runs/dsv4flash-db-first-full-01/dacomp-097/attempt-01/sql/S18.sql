SELECT segment, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown'
    END AS segment
  FROM intercom__company_enhanced
) GROUP BY segment
ORDER BY cnt DESC