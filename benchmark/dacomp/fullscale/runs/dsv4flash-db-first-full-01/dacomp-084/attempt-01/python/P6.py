import numpy as np
import pandas as pd

# Re-pull data including organization_name
ov = db.query("""
SELECT organization_id, organization_name, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)
ov_df['rn'] = ov_df.groupby('organization_size_category', observed=True)['organization_health_score'].rank(method='first', ascending=False)
ov_df['n'] = ov_df.groupby('organization_size_category', observed=True)['organization_id'].transform('count')
ov_df['top10'] = ov_df['rn'] <= np.ceil(ov_df['n'] * 0.1)

top10_detail = ov_df[ov_df['top10']][['organization_id','organization_size_category',
    'organization_name','current_active_employees','organization_health_score',
    'performance_category','management_ratio','avg_employee_performance_score',
    'position_fill_rate','annual_turnover_rate','organization_type','staffing_model',
    'organization_maturity_level']].sort_values(['organization_size_category','organization_health_score'], ascending=[True,False])
top10_detail.to_csv('top10_detail.csv', index=False)
print(top10_detail.to_string())
print()

# Common characteristics across all top10% orgs
print("=== Common characteristics across all 14 top-10% orgs ===")
print("All Excellent:", (top10_detail['performance_category']=='Excellent').all())
print("Avg perf score range:", top10_detail['avg_employee_performance_score'].min(), "-", top10_detail['avg_employee_performance_score'].max())
print("Avg fill rate range:", top10_detail['position_fill_rate'].min(), "-", top10_detail['position_fill_rate'].max())
print("Avg turnover range:", top10_detail['annual_turnover_rate'].min(), "-", top10_detail['annual_turnover_rate'].max())
print("Staffing model distribution:\n", top10_detail['staffing_model'].value_counts())
print("Maturity distribution:\n", top10_detail['organization_maturity_level'].value_counts())