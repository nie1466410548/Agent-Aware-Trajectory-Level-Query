-- Count conversations that don't match a company
WITH conv AS (
  SELECT DISTINCT ce.conversation_id, ce.all_contact_company_names AS company_name
  FROM intercom__conversation_enhanced ce
)
SELECT COUNT(*) AS unmatched_convs
FROM conv c
LEFT JOIN intercom__company_enhanced co ON c.company_name = co.company_name
WHERE co.company_id IS NULL