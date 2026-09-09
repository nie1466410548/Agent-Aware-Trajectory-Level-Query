WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  organization_sub_type,
  COUNT(*) as total,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) as attrition_pct
FROM emp
GROUP BY organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY attrition_pct DESC
LIMIT 10