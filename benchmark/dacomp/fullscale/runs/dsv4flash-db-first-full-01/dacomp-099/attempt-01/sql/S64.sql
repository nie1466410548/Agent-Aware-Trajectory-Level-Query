-- Use Upgrade Opportunity / Downgrade Risk conversation tags as event markers
SELECT event_type, COUNT(*) as total_convs, COUNT(DISTINCT company_name) as companies
FROM (
  SELECT all_contact_company_names as company_name, conversation_created_at,
         CASE WHEN all_conversation_tags LIKE '%Upgrade Opportunity%' THEN 'upgrade'
              WHEN all_conversation_tags LIKE '%Downgrade Risk%' THEN 'downgrade'
              ELSE NULL END as event_type
  FROM intercom__conversation_enhanced
  WHERE all_conversation_tags LIKE '%Upgrade Opportunity%' OR all_conversation_tags LIKE '%Downgrade Risk%'
)
WHERE event_type IS NOT NULL
GROUP BY event_type