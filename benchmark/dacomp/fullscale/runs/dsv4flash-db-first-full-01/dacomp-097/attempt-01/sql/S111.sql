-- Summary of dataset
SELECT 
  (SELECT COUNT(*) FROM intercom__company_enhanced) AS companies,
  (SELECT COUNT(DISTINCT company_name) FROM intercom__company_enhanced) AS distinct_companies,
  (SELECT COUNT(*) FROM intercom__contact_enhanced) AS contacts,
  (SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__contact_enhanced) AS contact_companies,
  (SELECT COUNT(*) FROM intercom__conversation_metrics) AS conversations,
  (SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__conversation_enhanced) AS conv_companies