-- Check which events have conversations in the 30-day window
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
)
SELECT e.event_type, 
  COUNT(*) as total_events,
  SUM(CASE WHEN e.event_at >= (SELECT MIN(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) + 30
           AND e.event_at <= (SELECT MAX(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) - 30 THEN 1 ELSE 0 END) as events_with_30d_buffer
FROM events e
GROUP BY e.event_type