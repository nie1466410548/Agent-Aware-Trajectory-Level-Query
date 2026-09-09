-- Check per-company conversation time ranges and event counts in window
WITH conv_range AS (
  SELECT all_contact_company_names as company_name, 
         MIN(conversation_created_at) as min_c, MAX(conversation_created_at) as max_c,
         COUNT(*) as n_convs
  FROM intercom__conversation_enhanced
  GROUP BY all_contact_company_names
),
tiers AS (
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
)
SELECT cr.company_name, cr.min_c, cr.max_c, cr.n_convs,
       SUM(CASE WHEN e.event_type='upgrade' THEN 1 ELSE 0 END) as n_upgrade,
       SUM(CASE WHEN e.event_type='downgrade' THEN 1 ELSE 0 END) as n_downgrade
FROM conv_range cr
LEFT JOIN events e ON e.company_name = cr.company_name
GROUP BY cr.company_name
ORDER BY cr.n_convs DESC