WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
)
SELECT 
  CASE WHEN tier > prev_tier THEN 'upgrade' WHEN tier < prev_tier THEN 'downgrade' ELSE 'no_change' END AS event_type,
  COUNT(*) AS events
FROM ordered
WHERE prev_tier IS NOT NULL
GROUP BY event_type