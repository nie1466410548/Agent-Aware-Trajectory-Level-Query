SELECT COUNT(*) AS overlap_with_companies FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__conversation_enhanced
  INTERSECT
  SELECT DISTINCT company_name AS cn FROM intercom__company_enhanced
)