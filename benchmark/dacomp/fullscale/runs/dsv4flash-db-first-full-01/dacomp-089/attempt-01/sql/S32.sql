-- Department distribution for key accounts
SELECT 
  c.account_id,
  c.department,
  c.title,
  CASE WHEN LOWER(c.title) LIKE '%chief%' AND (
    LOWER(c.title) LIKE '%executive%' OR LOWER(c.title) LIKE '%officer%' OR LOWER(c.title) LIKE '%technology%' 
    OR LOWER(c.title) LIKE '%marketing%' OR LOWER(c.title) LIKE '%operating%' OR LOWER(c.title) LIKE '%financial%'
    OR LOWER(c.title) LIKE '%strategy%' OR LOWER(c.title) LIKE '%staff%'
  ) THEN 1 ELSE 0 END AS is_c_level
FROM salesforce__contact_enhanced c
WHERE c.account_id IN (
  SELECT a.account_id FROM salesforce__customer_360_view a WHERE a.annual_revenue >= 71234915
)