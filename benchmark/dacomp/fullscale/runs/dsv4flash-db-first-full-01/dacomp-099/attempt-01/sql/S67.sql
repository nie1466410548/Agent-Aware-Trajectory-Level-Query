
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_created_at,
         LEAD(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS next_created_at
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_created_at, next_created_at,
       prev_plan, plan_name AS new_plan, prev_tier, tier,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
