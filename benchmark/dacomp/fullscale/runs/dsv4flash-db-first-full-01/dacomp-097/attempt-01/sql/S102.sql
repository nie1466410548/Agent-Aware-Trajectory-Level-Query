-- Segment composition of seats 420+ customers
SELECT 
  CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
       WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
       WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
       WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
       ELSE 'unknown' END AS segment,
  COUNT(*) AS total
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%seat_bucket:seats:420_plus%'
GROUP BY 1
ORDER BY total DESC