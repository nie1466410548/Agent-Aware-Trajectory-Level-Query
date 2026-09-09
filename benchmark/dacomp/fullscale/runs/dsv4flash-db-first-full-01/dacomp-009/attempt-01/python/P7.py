import json, numpy as np, pandas as pd

with open('/results/S33.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
dfm = pd.DataFrame(rows)
dfm.columns = ['Employee ID','month','days','units','pass_rate']

# Pivot to compare April vs May for each employee
dfm_pivot = dfm.pivot_table(index='Employee ID', columns='month', values=['units','pass_rate','days'], aggfunc='first')
print("Monthly data shape:", dfm_pivot.shape)
print(dfm_pivot.head())

# Correlation between April and May units
april_u = dfm[dfm.month=='2025-04'].set_index('Employee ID')['units']
may_u = dfm[dfm.month=='2025-05'].set_index('Employee ID')['units']
common = april_u.index.intersection(may_u.index)
print(f"\nEmployees with both months: {len(common)}")
print(f"Correlation April vs May units: r = {april_u[common].corr(may_u[common]):.3f}")

april_p = dfm[dfm.month=='2025-04'].set_index('Employee ID')['pass_rate']
may_p = dfm[dfm.month=='2025-05'].set_index('Employee ID')['pass_rate']
print(f"Correlation April vs May pass_rate: r = {april_p[common].corr(may_p[common]):.3f}")

# Top 10 employees and their month-over-month ranks
# Get the full ranking from S27
with open('/results/S27.rows.jsonl') as f:
    rows2 = [json.loads(l) for l in f]
df_rank = pd.DataFrame(rows2)
df_rank.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
                   'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']

print("\n=== Top 10 Employees: Month-over-Month Units ===")
top10_ids = df_rank[df_rank['rank']<=10]['Employee ID'].tolist()
for eid in top10_ids:
    emp = df_rank[df_rank['Employee ID']==eid]['Employee'].iloc[0]
    mdata = dfm[dfm['Employee ID']==eid]
    vals = {r['month']: f"{r['units']:.0f} (pass {r['pass_rate']}%)" for _, r in mdata.iterrows()}
    print(f"  {emp:12s}: {vals}")

# Within-month rank correlation
print("\n=== Within-month ranks for Top 10 employees ===")
for month in ['2025-04','2025-05']:
    month_data = dfm[dfm.month==month].copy()
    month_data['units_rank'] = month_data['units'].rank(ascending=False)
    month_data['pass_rank'] = month_data['pass_rate'].rank(ascending=False)
    month_data['combined_rank'] = (month_data['units_rank'] + month_data['pass_rank']).rank()
    # Get top 10 rank by combined rank
    top10_month = month_data.sort_values('combined_rank').head(10)
    emp_names = df_rank.set_index('Employee ID')['Employee'].to_dict()
    top10_month['Employee'] = top10_month['Employee ID'].map(emp_names)
    print(f"\n{month} Top 10 by units+pass rank:")
    for _, r in top10_month.iterrows():
        print(f"  {r['Employee']:12s}: units={r['units']:.0f}, pass={r['pass_rate']}%, combined_rank={r['combined_rank']:.0f}")