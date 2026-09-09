
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at,
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
         CASE WHEN tier > prev_tier THEN 1 ELSE -1 END AS delta
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
)
SELECT company_name, SUM(delta) AS net_direction, COUNT(*) as n_changes
FROM events
GROUP BY company_name
