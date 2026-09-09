SELECT 
  MIN(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS min_ratio,
  MAX(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS max_ratio,
  AVG(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS avg_ratio
FROM salesforce__customer_360_view