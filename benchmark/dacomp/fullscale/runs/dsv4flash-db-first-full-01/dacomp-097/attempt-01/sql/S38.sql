-- Check if multiple contacts can belong to same company
SELECT all_contact_company_names, COUNT(DISTINCT contact_id) as contact_count
FROM intercom__contact_enhanced
GROUP BY all_contact_company_names
ORDER BY contact_count DESC
LIMIT 10