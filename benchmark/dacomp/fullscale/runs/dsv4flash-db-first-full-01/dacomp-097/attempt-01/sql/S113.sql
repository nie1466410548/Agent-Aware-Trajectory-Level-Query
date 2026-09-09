-- Monthly volume by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  co.segment,
  strftime('%Y-%m', ce.conversation_created_at) AS month,
  COUNT(*) AS total_convs
FROM intercom__conversation_enhanced ce
JOIN company_dim co ON ce.all_contact_company_names = co.company_name
GROUP BY co.segment, month
ORDER BY co.segment, month