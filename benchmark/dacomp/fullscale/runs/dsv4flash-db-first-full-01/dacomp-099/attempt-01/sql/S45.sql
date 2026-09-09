-- Per-event detailed metrics
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
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type,
         ROW_NUMBER() OVER (PARTITION BY company_name ORDER BY created_at) AS event_seq
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at