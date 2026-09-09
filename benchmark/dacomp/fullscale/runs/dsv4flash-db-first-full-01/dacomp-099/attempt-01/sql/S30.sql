SELECT ce.company_id, ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count, ce.all_company_tags
FROM intercom__company_enhanced ce
WHERE ce.company_name IN (
  SELECT all_contact_company_names FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
)