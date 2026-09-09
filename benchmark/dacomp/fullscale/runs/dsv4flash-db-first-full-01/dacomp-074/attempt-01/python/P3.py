import pandas as pd, numpy as np
d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])

# Examine DSO & overdue around transition: for each sub, show periods first_high_idx-3 .. first_high_idx+2
print("=== AR trajectory around High transition ===")
for sub in d['subsidiary_id'].unique():
    s = d[d['subsidiary_id']==sub].sort_values('period_idx')
    fh = s['first_high_idx'].iloc[0]
    win = s[(s['period_idx']>=fh-3) & (s['period_idx']<=fh+1)]
    print(f"\n{sub} (first High period {fh}):")
    for _,r in win.iterrows():
        print(f"  p{int(r['period_idx'])} {str(r['dashboard_date'])[:10]} risk={r['cash_flow_risk_level']:<6} DSO={r['weighted_average_days_outstanding']:6.1f} overdue%={r['overdue_percentage']:5.1f} rev={r['revenue']:,.0f} exp={r['expense']:,.0f}")

# Check DSO max in pre-high window
pre = d[d['is_prehigh']]
print("\n=== DSO values in pre-high windows ===")
print(pre.groupby('subsidiary_id')['weighted_average_days_outstanding'].agg(['min','max','mean']))

print("\n=== Overdue values in pre-high windows ===")
print(pre.groupby('subsidiary_id')['overdue_percentage'].agg(['min','max','mean']))

# Check DSO in months before High
print("\n=== DSO by months-to-high (include transition month as month 0) ===")
d['months_to_high'] = d['first_high_idx'] - d['period_idx']
mt = d[(d['months_to_high']>=0) & (d['months_to_high']<=7)].groupby('months_to_high').agg(
    dso_mean=('weighted_average_days_outstanding','mean'),
    dso_gt45=('dso_gt45','mean'),
    overdue_mean=('overdue_percentage','mean'),
    rev_fluct=('rev_fluct','mean'),
    overdue_rise=('overdue_rise','mean')
).reset_index().sort_values('months_to_high', ascending=False)
print(mt.to_string())

# Where does DSO cross 45? Check the transition month
print("\n=== DSO at transition (first High month) ===")
trans = d[d['cash_flow_risk_level']=='High'].groupby('subsidiary_id').first().reset_index()
print(trans[['subsidiary_id','first_high_idx','weighted_average_days_outstanding','overdue_percentage']].to_string())

# Healthy periods DSO
healthy = d[d['is_healthy']]
print("\nHealthy DSO stats:", healthy['weighted_average_days_outstanding'].describe().round(1).to_dict())

# What does 'Medium' look like vs pre-high?
med = d[d['cash_flow_risk_level']=='Medium']
print("\nMedium DSO stats:", med['weighted_average_days_outstanding'].describe().round(1).to_dict())
print("Medium overdue%:", med['overdue_percentage'].describe().round(2).to_dict())

# Full healthy comparison - group definitions
# Healthy = Low risk periods that are NOT within 2 months before High (to avoid contamination)
d['group'] = 'other'
d.loc[d['is_healthy'],'group'] = 'healthy_low'
d.loc[d['is_prehigh'],'group'] = 'prehigh'
print("\n=== Group counts ===")
print(d['group'].value_counts())

# Compare prehigh vs healthy_low
print("\n=== PreHigh vs HealthyLow (rev_fluct) ===")
print(d.groupby('group')['rev_fluct'].mean())
print("\n=== PreHigh vs HealthyLow (DSO) ===")
print(d.groupby('group')['weighted_average_days_outstanding'].mean())
print("\n=== PreHigh vs HealthyLow (overdue) ===")
print(d.groupby('group')['overdue_percentage'].mean())
print("\n=== PreHigh vs HealthyLow (divergence) ===")
print(d.groupby('group')['divergence'].mean())

# expense control: expense growth vs revenue growth separately
print("\n=== Revenue growth by group ===")
print(d.groupby('group')['rev_chg'].mean())
print("\n=== Expense growth by group ===")
print(d.groupby('group')['exp_chg'].mean())

# How often does expense growth exceed revenue growth by > 20pp in prehigh vs healthy?
d['exp_outgrow_rev'] = (d['exp_chg'] - d['rev_chg']) > 0.20
print("\n=== Expense outgrows revenue by >20pp rate ===")
print(d.groupby('group')['exp_outgrow_rev'].mean())

# Also: expense-to-revenue ratio
d['exp_rev_ratio'] = d['expense']/d['revenue']
print("\n=== Expense/Revenue ratio by group ===")
print(d.groupby('group')['exp_rev_ratio'].mean())
