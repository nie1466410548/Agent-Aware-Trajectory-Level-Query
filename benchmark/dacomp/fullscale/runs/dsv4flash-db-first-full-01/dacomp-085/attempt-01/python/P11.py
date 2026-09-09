import pandas as pd

crit = pd.read_csv('/work/priority_ranking.csv')
print("Critical group (79) metrics:")
print(f"Shift-required count: {crit['is_work_shift_required'].sum()}")
print(f"Shift ratio: {crit['is_work_shift_required'].mean():.3f}")
print(f"Median saturation: {crit['talent_saturation'].median():.3f}")
print(f"Median hours: {crit['avg_weekly_hours'].median():.1f}")
print(f"Median health: {crit['job_health_score'].median():.1f}")
print(f"Median dev: {crit['avg_career_development_score'].median():.2f}")
print(f"Tier1 count: {(crit['job_value_tier']=='Tier 1').sum()}, Tier2: {(crit['job_value_tier']=='Tier 2').sum()}")

# Job family grouping (simplified by title keywords)
kw_map = {
    'Security': 'Security Engineering',
    'ML/Data': 'ML / Data Science',
    'DevOps': 'DevOps / Infrastructure',
    'Software/Backend/Frontend/Developer': 'Software Development',
    'Product': 'Product Management',
    'Sales': 'Sales',
    'HR': 'HR',
    'UX/Design': 'Design/UX',
}
import re
def classify(t):
    t_low = t.lower()
    if 'security' in t_low: return 'Security Engineering'
    if 'machine learning' in t_low or 'data scientist' in t_low or 'data' in t_low: return 'ML / Data'
    if 'devops' in t_low: return 'DevOps / Infrastructure'
    if 'developer' in t_low or 'engineer' in t_low: return 'Software Development'
    if 'product manager' in t_low: return 'Product Management'
    if 'sales' in t_low: return 'Sales'
    if 'hr' in t_low or 'human resource' in t_low: return 'HR'
    if 'ux' in t_low or 'design' in t_low: return 'Design/UX'
    return 'Other'

crit['family'] = crit['job_title'].apply(classify)
print("\nCritical profiles by functional family:")
print(crit['family'].value_counts().to_string())
