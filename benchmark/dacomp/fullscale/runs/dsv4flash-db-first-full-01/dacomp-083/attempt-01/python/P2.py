import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ===== Tiered Recommendation Priority Matrix =====
result = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  CASE WHEN highest_management_level_reached = 0 THEN 'IC (L0)'
       WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)'
       WHEN highest_management_level_reached = 2 THEN 'Manager (L2)'
       ELSE 'Sr Mgmt (L3+)' END as mgmt_tier,
  dept_performance_category,
  COUNT(*) as n_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as n_at_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as at_risk_pct
FROM core
GROUP BY mgmt_tier, dept_performance_category
""")
tier_df = db.frame(result)

# Compute a priority score = at-risk pct * sqrt(n) to balance rate and volume
tier_df['priority_score'] = tier_df['at_risk_pct'] * np.sqrt(tier_df['n_core'])
tier_df['priority_label'] = pd.cut(tier_df['priority_score'], bins=[0, 100, 200, 400, 1000],
                                    labels=['Low', 'Medium', 'High', 'Critical'])
print("Tiered recommendation matrix with priority:")
print(tier_df.sort_values('priority_score', ascending=False).to_string())

# Pivot heatmap of at-risk pct by mgmt tier and dept perf
pivot_pct = tier_df.pivot(index='mgmt_tier', columns='dept_performance_category', values='at_risk_pct')
# reorder for display
pivot_pct = pivot_pct.reindex(['IC (L0)', 'Team Lead (L1)', 'Manager (L2)', 'Sr Mgmt (L3+)'])
pivot_pct = pivot_pct[['Good', 'Average', 'Needs Improvement']]

fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(pivot_pct, annot=True, fmt='.1f', cmap='RdYlGn_r', ax=ax, linewidths=0.5,
            cbar_kws={'label': 'At-Risk % among Core Employees'}, vmin=0, vmax=45)
ax.set_title('Priority Matrix: At-Risk % by Management Tier & Dept Performance', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/priority_matrix.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved priority_matrix.png")

# ===== Attrition risk by org sub type =====
result2 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT organization_sub_type, COUNT(*) as total,
       SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
       ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / COUNT(*), 1) as attrition_pct
FROM emp
GROUP BY organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY attrition_pct DESC
""")
org_risk_df = db.frame(result2)
print("\nAttrition risk by org sub type:")
print(org_risk_df.to_string())

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(org_risk_df['organization_sub_type'], org_risk_df['attrition_pct'], 
        color=['#C44E52' if v >= 4 else '#DD8452' if v >= 3 else '#4C72B0' for v in org_risk_df['attrition_pct']])
ax.set_xlabel('High-Value Attrition Risk %')
ax.set_ylabel('Organization Sub Type')
ax.set_title('High-Value Attrition Risk % by Organization Sub Type', fontsize=14, fontweight='bold')
for i, v in enumerate(org_risk_df['attrition_pct']):
    ax.text(v + 0.05, i, f'{v:.1f}%', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/attrition_by_org.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved attrition_by_org.png")

print("\nDone!")
