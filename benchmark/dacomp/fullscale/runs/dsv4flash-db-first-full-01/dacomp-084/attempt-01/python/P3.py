import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Pull data
ov = db.query("""
SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
pf = db.query("""
SELECT organization_id, avg_employee_satisfaction_proxy, high_achiever_percentage,
       avg_weekly_hours_per_employee
FROM workday__organization_performance
""")
pf_df = db.frame(pf)
ov_df = ov_df.merge(pf_df, on='organization_id', how='left')

tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)

# 1. Health score distribution
dist = ov_df.groupby('organization_size_category', observed=True)['organization_health_score'].agg(
    n='count', mean='mean', median='median', std='std', min='min', max='max',
    q25=lambda x: x.quantile(0.25), q75=lambda x: x.quantile(0.75))
print("=== Health score distribution per tier ===")
print(dist.round(2))

# 2. Performance category composition
comp = ov_df.groupby(['organization_size_category','performance_category'], observed=True).size().unstack(fill_value=0)
comp_pct = comp.div(comp.sum(axis=1), axis=0) * 100
print("\n=== Performance category composition (% orgs) ===")
print(comp_pct.round(1))

# 3. Management ratio stats
mr = ov_df.groupby('organization_size_category', observed=True)['management_ratio'].agg(['count','mean','std','min','max'])
print("\n=== Management ratio stats per tier ===")
print(mr.round(3))

# Save a figure: health score distribution by tier (boxplot) + composition stacked bar
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=ov_df, x='organization_size_category', y='organization_health_score', ax=axes[0],
            palette='viridis')
axes[0].set_title('Organization Health Score by Size Tier')
axes[0].tick_params(axis='x', rotation=20)

comp_pct.plot(kind='bar', stacked=True, ax=axes[1], color=['#2e8b57','#ffd700','#dc143c','#4682b4'])
axes[1].set_title('Performance Category Composition by Size Tier')
axes[1].set_ylabel('% of organizations')
axes[1].tick_params(axis='x', rotation=20)
axes[1].legend(title='Performance Category', bbox_to_anchor=(1.02,1), loc='upper left')
plt.tight_layout()
plt.savefig('tier_health_and_composition.png', dpi=110)
print("\nSaved tier_health_and_composition.png")

# Save data tables for report
dist.round(2).to_csv('health_distribution.csv')
comp_pct.round(1).to_csv('performance_composition.csv')
print("Saved CSVs")