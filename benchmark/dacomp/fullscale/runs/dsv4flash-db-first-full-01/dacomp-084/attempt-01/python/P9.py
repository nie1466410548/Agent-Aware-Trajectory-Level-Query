import numpy as np
import pandas as pd
import scipy.stats as stats

ov = db.query("""
SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)

# Correlations overall
cols = ['organization_health_score','management_ratio','avg_employee_performance_score','position_fill_rate','annual_turnover_rate']
corr = ov_df[cols].corr().round(3)
print("=== Overall correlation matrix ===")
print(corr)

# Correlation within each tier between MR and health
print("\n=== MR vs Health correlation per tier ===")
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    r, p = stats.pearsonr(tdf['management_ratio'], tdf['organization_health_score'])
    print(f"{tier}: r={r:.3f}, p={p:.3f}, n={len(tdf)}")

# MR vs performance correlation
print("\n=== MR vs Performance score correlation per tier ===")
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    r, p = stats.pearsonr(tdf['management_ratio'], tdf['avg_employee_performance_score'])
    print(f"{tier}: r={r:.3f}, p={p:.3f}")

# Fill rate and turnover correlations with health
print("\n=== Fill rate & turnover vs Health (overall) ===")
for c in ['position_fill_rate','annual_turnover_rate','avg_employee_performance_score']:
    r, p = stats.pearsonr(ov_df[c], ov_df['organization_health_score'])
    print(f"{c}: r={r:.3f}, p={p:.3f}")