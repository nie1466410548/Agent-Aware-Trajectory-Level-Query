-- Per-event before/after counts including zero-conversation windows
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
SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
  SUM(CASE WHEN c.conversation_created_at < e.event_at THEN 1 ELSE 0 END) AS before_convs,
  SUM(CASE WHEN c.conversation_created_at > e.event_at THEN 1 ELSE 0 END) AS after_convs,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) AS before_bugs,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) AS after_bugs,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) AS before_outages,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) AS after_outages,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) AS before_esc,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) AS after_esc,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.sla_status='breached' THEN 1 ELSE 0 END) AS before_sla,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.sla_status='breached' THEN 1 ELSE 0 END) AS after_sla
FROM events e
LEFT JOIN intercom__conversation_enhanced c 
  ON c.all_contact_company_names = e.company_name
  AND c.conversation_created_at >= datetime(e.event_at, '-30 days')
  AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
  AND c.conversation_created_at != e.event_at
GROUP BY e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan
ORDER BY e.event_type, e.company_name, e.event_at