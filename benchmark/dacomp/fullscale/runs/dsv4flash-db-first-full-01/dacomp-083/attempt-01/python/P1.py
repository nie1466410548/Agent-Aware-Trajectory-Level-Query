import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get core employee data
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
SELECT age, tenure_years, total_positions_held, total_promotions, lateral_moves, management_positions_held, 
       overall_employee_score, career_development_score, retention_stability_score,
       marital_status, ethnicity_codes, career_phase, employee_maturity_segment,
       employee_risk_level, compensation_tier, work_conditions_score, dept_turnover_rate,
       dept_health_score, dept_management_ratio, organization_type, organization_sub_type,
       dept_performance_category, highest_management_level_reached,
       is_work_shift_required, is_union_eligible, employee_value_segment
FROM core
""")
core_df = db.frame(result)

print(f"Core employees: {len(core_df)}")
print(f"\nNumerical features stats:")
numerical = ['age', 'tenure_years', 'total_positions_held', 'total_promotions', 'lateral_moves', 
             'management_positions_held', 'overall_employee_score', 'career_development_score',
             'retention_stability_score', 'work_conditions_score', 'dept_turnover_rate', 'dept_health_score']
stats = core_df[numerical].describe().T
stats['std'] = core_df[numerical].std()
print(stats[['mean', 'std', 'min', 'max']].round(2))

# Also get all employees for comparison
result2 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT age, tenure_years, overall_employee_score, career_development_score, retention_stability_score,
       employee_risk_level, total_positions_held, total_promotions, lateral_moves, management_positions_held
FROM emp
""")
all_df = db.frame(result2)
print(f"\nAll employees: {len(all_df)}")

# ===== VISUALIZATION 1: Core Employee Age Distribution =====
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Core Employees Profile Analysis', fontsize=16, fontweight='bold')

# Age histogram
axes[0, 0].hist(core_df['age'], bins=20, color='steelblue', edgecolor='white', alpha=0.8)
axes[0, 0].axvline(core_df['age'].mean(), color='red', linestyle='--', label=f"Mean: {core_df['age'].mean():.1f}")
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title(f'Age Distribution (n={len(core_df)})')
axes[0, 0].legend()

# Tenure histogram
axes[0, 1].hist(core_df['tenure_years'], bins=20, color='coral', edgecolor='white', alpha=0.8)
axes[0, 1].axvline(core_df['tenure_years'].mean(), color='red', linestyle='--', label=f"Mean: {core_df['tenure_years'].mean():.2f}")
axes[0, 1].set_xlabel('Tenure Years')
axes[0, 1].set_ylabel('Count')
axes[0, 1].set_title('Tenure Distribution')
axes[0, 1].legend()

# Marital status
marital_counts = core_df['marital_status'].value_counts()
axes[0, 2].bar(marital_counts.index, marital_counts.values, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
axes[0, 2].set_xlabel('Marital Status')
axes[0, 2].set_ylabel('Count')
axes[0, 2].set_title('Marital Status Distribution')
for i, v in enumerate(marital_counts.values):
    axes[0, 2].text(i, v + 5, f'{v}\n({100*v/len(core_df):.1f}%)', ha='center', fontsize=9)

# Ethnicity
ethnic_counts = core_df['ethnicity_codes'].value_counts()
axes[1, 0].bar(ethnic_counts.index, ethnic_counts.values, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#937860', '#8172B2'])
axes[1, 0].set_xlabel('Ethnicity')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Ethnicity Distribution')
axes[1, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(ethnic_counts.values):
    axes[1, 0].text(i, v + 5, f'{v}\n({100*v/len(core_df):.1f}%)', ha='center', fontsize=8)

# Career phase
phase_counts = core_df['career_phase'].value_counts()
axes[1, 1].bar(phase_counts.index, phase_counts.values, color=['#4C72B0', '#DD8452', '#55A868'])
axes[1, 1].set_xlabel('Career Phase')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Career Phase Distribution')
for i, v in enumerate(phase_counts.values):
    axes[1, 1].text(i, v + 5, f'{v}\n({100*v/len(core_df):.1f}%)', ha='center', fontsize=9)

# Maturity segment
mat_counts = core_df['employee_maturity_segment'].value_counts()
axes[1, 2].bar(mat_counts.index, mat_counts.values, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
axes[1, 2].set_xlabel('Maturity Segment')
axes[1, 2].set_ylabel('Count')
axes[1, 2].set_title('Maturity Segment Distribution')
for i, v in enumerate(mat_counts.values):
    axes[1, 2].text(i, v + 5, f'{v}\n({100*v/len(core_df):.1f}%)', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/core_employees_profile.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved core_employees_profile.png")

# ===== VISUALIZATION 2: Cross-group Risk Analysis Heatmap =====
result3 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT career_phase, employee_maturity_segment, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
       SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) as med_risk,
       SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk
FROM core
GROUP BY career_phase, employee_maturity_segment
ORDER BY career_phase, employee_maturity_segment
""")
cross_df = db.frame(result3)
print("\nCross-group analysis:")
print(cross_df.to_string())

# Create pivot table for high risk percentage
pivot_high = cross_df.pivot(index='career_phase', columns='employee_maturity_segment', values='high_risk').fillna(0)
pivot_total = cross_df.pivot(index='career_phase', columns='employee_maturity_segment', values='total').fillna(0)
pivot_pct = (pivot_high / pivot_total * 100).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_pct, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, 
            linewidths=0.5, cbar_kws={'label': 'High Risk %'})
ax.set_title('High Risk Core Employees by Career Phase & Maturity Segment', fontsize=14, fontweight='bold')
ax.set_xlabel('Employee Maturity Segment')
ax.set_ylabel('Career Phase')
plt.tight_layout()
plt.savefig('/work/risk_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved risk_heatmap.png")

# ===== VISUALIZATION 3: High-value attrition risk comparison =====
result4 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT employee_value_segment, COUNT(*) as cnt
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
GROUP BY employee_value_segment
ORDER BY cnt DESC
""")
high_value_risk_df = db.frame(result4)
print("\nHigh-value attrition risk employees by value segment:")
print(high_value_risk_df.to_string())

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#C44E52', '#4C72B0', '#55A868', '#DD8452', '#937860', '#8172B2']
bars = ax.bar(high_value_risk_df['employee_value_segment'], high_value_risk_df['cnt'], 
              color=colors[:len(high_value_risk_df)])
ax.set_xlabel('Employee Value Segment')
ax.set_ylabel('Count')
ax.set_title('High-Value Attrition Risk Employees by Value Segment', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
for i, v in enumerate(high_value_risk_df['cnt']):
    ax.text(i, v + 5, str(v), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('/work/high_value_attrition_risk.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved high_value_attrition_risk.png")

# ===== VISUALIZATION 4: Organizational environment factors for risk levels =====
result5 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT employee_risk_level, 
       AVG(work_conditions_score) as avg_work_cond,
       AVG(dept_turnover_rate) as avg_turnover,
       AVG(dept_health_score) as avg_dept_health
FROM core
GROUP BY employee_risk_level
ORDER BY employee_risk_level
""")
risk_env_df = db.frame(result5)
print("\nOrganizational environment by risk level:")
print(risk_env_df.to_string())

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Organizational Environment Factors by Risk Level (Core Employees)', fontsize=14, fontweight='bold')

risk_levels = risk_env_df['employee_risk_level']
axes[0].bar(risk_levels, risk_env_df['avg_work_cond'], color=['#55A868', '#DD8452', '#C44E52'])
axes[0].set_ylabel('Avg Work Conditions Score')
axes[0].set_title('Work Conditions')

axes[1].bar(risk_levels, risk_env_df['avg_turnover'], color=['#55A868', '#DD8452', '#C44E52'])
axes[1].set_ylabel('Avg Dept Turnover Rate')
axes[1].set_title('Department Turnover Rate')

axes[2].bar(risk_levels, risk_env_df['avg_dept_health'], color=['#55A868', '#DD8452', '#C44E52'])
axes[2].set_ylabel('Avg Dept Health Score')
axes[2].set_title('Department Health Score')

plt.tight_layout()
plt.savefig('/work/risk_environment_factors.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved risk_environment_factors.png")

# ===== VISUALIZATION 5: Compensation tier distribution for core employees =====
result6 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT compensation_tier, COUNT(*) as cnt
FROM core
GROUP BY compensation_tier
ORDER BY cnt DESC
""")
comp_df = db.frame(result6)
print("\nCompensation tier distribution:")
print(comp_df.to_string())

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(comp_df['compensation_tier'], comp_df['cnt'], color=['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#937860'])
ax.set_xlabel('Compensation Tier')
ax.set_ylabel('Count')
ax.set_title('Core Employees by Compensation Tier', fontsize=12, fontweight='bold')
for i, v in enumerate(comp_df['cnt']):
    ax.text(i, v + 5, str(v), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('/work/compensation_tier_dist.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved compensation_tier_dist.png")

# ===== VISUALIZATION 6: Tiered recommendation system - management level vs dept performance =====
result7 = db.query("""
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT highest_management_level_reached, dept_performance_category, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as at_risk,
       SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention
FROM core
GROUP BY highest_management_level_reached, dept_performance_category
ORDER BY highest_management_level_reached, dept_performance_category
""")
tier_df = db.frame(result7)
print("\nTiered analysis:")
print(tier_df.to_string())

# Create pivot table for at-risk percentage
pivot_atrisk = tier_df.pivot(index='highest_management_level_reached', 
                              columns='dept_performance_category', values='at_risk').fillna(0)
pivot_total2 = tier_df.pivot(index='highest_management_level_reached', 
                              columns='dept_performance_category', values='total').fillna(0)
pivot_risk_pct = (pivot_atrisk / pivot_total2 * 100).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_risk_pct, annot=True, fmt='.1f', cmap='viridis', ax=ax,
            linewidths=0.5, cbar_kws={'label': 'At-Risk %'})
ax.set_title('Core Employee Risk % by Management Level & Dept Performance', fontsize=14, fontweight='bold')
ax.set_xlabel('Department Performance Category')
ax.set_ylabel('Highest Management Level Reached')
plt.tight_layout()
plt.savefig('/work/tiered_recommendation_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()
print("Saved tiered_recommendation_heatmap.png")

print("\nAll visualizations generated successfully!")