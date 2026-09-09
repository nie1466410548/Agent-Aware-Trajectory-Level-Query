-- First "Upgrade Opportunity" conversation per company (as hypothetical upgrade_at)
-- and first "Downgrade Risk" conversation per company (as hypothetical downgrade_at)
SELECT company_name, event_type, MIN(conversation_created_at) as first_event_at, COUNT(*) as tag_count
FROM (
  SELECT all_contact_company_names as company_name, conversation_created_at,
         CASE WHEN all_conversation_tags LIKE '%Upgrade Opportunity%' THEN 'upgrade'
              WHEN all_conversation_tags LIKE '%Downgrade Risk%' THEN 'downgrade' END as event_type
  FROM intercom__conversation_enhanced
  WHERE all_conversation_tags LIKE '%Upgrade Opportunity%' OR all_conversation_tags LIKE '%Downgrade Risk%'
)
WHERE event_type IS NOT NULL
GROUP BY company_name, event_type
ORDER BY company_name, event_type