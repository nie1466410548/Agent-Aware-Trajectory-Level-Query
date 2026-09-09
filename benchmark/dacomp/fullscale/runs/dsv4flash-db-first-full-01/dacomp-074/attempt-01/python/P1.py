
import json, pandas as pd, numpy as np

def load(rid):
    rows=[]
    with open(f'/results/S{rid}.rows.jsonl') as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

cols25 = ['subsidiary_id','dashboard_date','period_idx','cash_flow_risk_level',
          'weighted_average_days_outstanding','overdue_percentage','revenue','expense',
          'prev_revenue','prev_expense','prev_overdue','prev2_overdue']
d = pd.DataFrame(load(25), columns=cols25)
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])

# First high date per subsidiary
fh = pd.DataFrame(load(22), columns=['subsidiary_id','first_high_date'])
fh['first_high_date'] = pd.to_datetime(fh['first_high_date'])
d = d.merge(fh, on='subsidiary_id', how='left')

# Pre-High window: the 6 periods immediately before first High period (period_idx in [first_high_idx-6, first_high_idx-1])
first_high_idx = d[d['cash_flow_risk_level']=='High'].groupby('subsidiary_id')['period_idx'].min().rename('first_high_idx')
d = d.merge(first_high_idx, on='subsidiary_id', how='left')
d['is_prehigh'] = (d['period_idx'] >= d['first_high_idx']-6) & (d['period_idx'] < d['first_high_idx'])
d['is_healthy'] = (d['cash_flow_risk_level']=='Low')
d['is_high'] = (d['cash_flow_risk_level']=='High')

# Revenue MoM change %
d['rev_chg'] = (d['revenue'] - d['prev_revenue']) / d['prev_revenue'].abs()
d['exp_chg'] = (d['expense'] - d['prev_expense']) / d['prev_expense'].abs()
d['rev_fluct'] = d['rev_chg'].abs() > 0.20  # revenue fluctuation exceeding 20%
# Expense-revenue growth divergence (percentage-point difference)
d['divergence'] = d['exp_chg'] - d['rev_chg']
# AR flags
d['dso_gt45'] = d['weighted_average_days_outstanding'] > 45
d['overdue_rise'] = d['overdue_percentage'] > d['prev_overdue']
# 3 consecutive months overdue rising: current + previous two all rising (uses prev_overdue, prev2_overdue)
d['overdue_rise3'] = (d['overdue_percentage'] > d['prev_overdue']) & (d['prev_overdue'] > d['prev2_overdue'])

print("Rows:", len(d))
print(d[['subsidiary_id','period_idx','first_high_idx','is_prehigh']].head(20))
print("\nPre-high windows per sub:")
print(d[d['is_prehigh']].groupby('subsidiary_id')['period_idx'].agg(['min','max']))
print("\nHealthy (Low) period count per sub:")
print(d.groupby('subsidiary_id')['is_healthy'].sum())
d.to_csv('/work/metrics_all.csv', index=False)
print("Saved metrics_all.csv")
