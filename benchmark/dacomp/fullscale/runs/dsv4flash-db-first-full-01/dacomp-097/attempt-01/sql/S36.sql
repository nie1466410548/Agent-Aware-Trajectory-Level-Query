SELECT COUNT(*) AS overlap_contact_company FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__contact_enhanced
  INTERSECT
  SELECT DISTINCT company_name AS cn FROM intercom__company_enhanced
)