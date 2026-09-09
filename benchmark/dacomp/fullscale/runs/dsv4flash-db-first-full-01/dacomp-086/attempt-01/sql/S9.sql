SELECT 
  contacts_with_email * 1.0 / NULLIF(total_contacts, 0) AS contact_email_ratio
FROM salesforce__customer_360_view 
LIMIT 20