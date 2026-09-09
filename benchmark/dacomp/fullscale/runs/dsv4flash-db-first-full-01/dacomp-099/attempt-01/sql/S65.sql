SELECT company_name FROM (
  SELECT DISTINCT all_contact_company_names as company_name FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%'
  INTERSECT
  SELECT DISTINCT all_contact_company_names as company_name FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
) ORDER BY company_name