-- Check how many Chief contacts exist overall and in key accounts
SELECT 'All' AS scope, COUNT(*) AS cnt FROM salesforce__contact_enhanced WHERE title LIKE '%Chief%'
UNION ALL
SELECT 'Key Accounts', COUNT(*) FROM salesforce__contact_enhanced 
WHERE account_id IN (SELECT account_id FROM salesforce__customer_360_view WHERE annual_revenue >= 71234915)
  AND title LIKE '%Chief%'