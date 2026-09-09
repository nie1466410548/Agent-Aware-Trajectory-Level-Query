WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
),
tiers AS (
  SELECT 
    CASE WHEN highest_management_level_reached = 0 THEN 'Individual Contributor (L0)'
         WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)'
         WHEN highest_management_level_reached = 2 THEN 'Manager (L2)'
         ELSE 'Senior Management (L3+)' END as mgmt_tier,
    dept_performance_category,
    COUNT(*) as n_core,
    SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as n_at_risk,
    SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as n_low_retention,
    ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as at_risk_pct,
    ROUND(AVG(overall_employee_score), 1) as avg_overall,
    ROUND(AVG(career_development_score), 1) as avg_career,
    ROUND(AVG(retention_stability_score), 1) as avg_retention
  FROM core
  GROUP BY mgmt_tier, dept_performance_category
)
SELECT * FROM tiers
ORDER BY at_risk_pct DESC, n_core DESC