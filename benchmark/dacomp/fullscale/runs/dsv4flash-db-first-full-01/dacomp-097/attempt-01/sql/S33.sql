SELECT COUNT(*) AS overlap_count FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__conversation_enhanced
  INTERSECT
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__contact_enhanced
)