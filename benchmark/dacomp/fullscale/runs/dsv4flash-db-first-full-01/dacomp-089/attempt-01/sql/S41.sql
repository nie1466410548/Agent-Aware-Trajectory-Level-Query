-- Check how many key accounts have Chief-level contacts
SELECT COUNT(DISTINCT c.account_id) AS accounts_with_chief
FROM salesforce__contact_enhanced c
WHERE c.account_id IN (SELECT a.account_id FROM salesforce__customer_360_view a WHERE a.annual_revenue >= 71234915)
  AND c.title LIKE '%Chief%'