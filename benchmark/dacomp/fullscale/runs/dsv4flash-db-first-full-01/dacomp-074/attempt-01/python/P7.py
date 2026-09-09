import pandas as pd, numpy as np

d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])
d['months_to_high'] = d['first_high_idx'] - d['period_idx']
d['prev_dso'] = d.groupby('subsidiary_id')['weighted_average_days_outstanding'].shift(1)

# When does DSO first cross 35 in the pre-high window?
print("=== DSO > 35 first occurrence (months before High) ===")
for sub in d['subsidiary_id'].unique():
    s = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    first35 = s[s['weighted_average_days_outstanding']>35]
    if len(first35):
        mt = first35.iloc[0]['months_to_high']
        dso = first35.iloc[0]['weighted_average_days_outstanding']
        print(f"{sub}: first DSO>35 at T-{int(mt)} (DSO={dso:.1f})")
    else:
        print(f"{sub}: DSO never exceeded 35 in pre-high window (max {s['weighted_average_days_outstanding'].max():.1f})")

# When does revenue fluctuation first occur?
print("\n=== First RevFluc>20% occurrence (months before High) ===")
for sub in d['subsidiary_id'].unique():
    s = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    firstf = s[s['rev_fluct']]
    if len(firstf):
        mt = firstf.iloc[0]['months_to_high']
        print(f"{sub}: first RevFluc at T-{int(mt)}")
    else:
        print(f"{sub}: no RevFluc in pre-high window")

# When does score >= 2 first appear?
print("\n=== First Score>=2 (DSO>35 or RevFluc or OverJump or Exp>Rev) occurrence ===")
d['score'] = ((d['weighted_average_days_outstanding']>35).astype(int) + d['rev_fluct'].astype(int) + 
              ((d['overdue_percentage']-d['prev_overdue'])>1).astype(int) + (d['exp_chg']>d['rev_chg']).astype(int))
for sub in d['subsidiary_id'].unique():
    s = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    f2 = s[s['score']>=2]
    if len(f2):
        print(f"{sub}: first score>=2 at T-{int(f2.iloc[0]['months_to_high'])}")
    else:
        print(f"{sub}: no score>=2 in pre-high window")

# Cash flow metrics comparison
print("\n=== Cash Flow Metrics: Pre-High vs Healthy ===")
# Load dashboard cash flow data from archived S23
import json
cols23 = ['subsidiary_id','dashboard_date','cash_flow_risk_level','cash_flow_health','overall_financial_health_score',
          'financial_health_grade','operating_cash_flow','net_cash_flow','overdue_percentage',
          'weighted_average_days_outstanding','total_ar_amount','overdue_amount','total_risk_score',
          'current_ratio','quick_ratio','net_profit_margin','gross_margin_ratio','return_on_equity']
cf = pd.DataFrame([json.loads(l) for l in open('/results/S23.rows.jsonl')], columns=cols23)
cf['dashboard_date'] = pd.to_datetime(cf['dashboard_date'])
cf = cf.merge(d[['subsidiary_id','dashboard_date','is_prehigh','months_to_high','period_idx','first_high_idx']], 
              on=['subsidiary_id','dashboard_date'], how='left')
cf['is_healthy'] = cf['cash_flow_risk_level']=='Low'

print("\nOperating cash flow: pre-high mean={:,.0f}, healthy mean={:,.0f}".format(
    cf[cf['is_prehigh']]['operating_cash_flow'].mean(), cf[cf['is_healthy']]['operating_cash_flow'].mean()))
print("Net cash flow: pre-high mean={:,.0f}, healthy mean={:,.0f}".format(
    cf[cf['is_prehigh']]['net_cash_flow'].mean(), cf[cf['is_healthy']]['net_cash_flow'].mean()))
print("Health score: pre-high mean={:.1f}, healthy mean={:.1f}".format(
    cf[cf['is_prehigh']]['overall_financial_health_score'].mean(), cf[cf['is_healthy']]['overall_financial_health_score'].mean()))
print("Current ratio: pre-high mean={:.2f}, healthy mean={:.2f}".format(
    cf[cf['is_prehigh']]['current_ratio'].mean(), cf[cf['is_healthy']]['current_ratio'].mean()))
print("Net profit margin: pre-high mean={:.4f}, healthy mean={:.4f}".format(
    cf[cf['is_prehigh']]['net_profit_margin'].mean(), cf[cf['is_healthy']]['net_profit_margin'].mean()))

# Cash flow by months-to-high
print("\nNet cash flow by months-to-high:")
cfm = cf[(cf['months_to_high']>=0)&(cf['months_to_high']<=7)].groupby('months_to_high').agg(
    net_cf=('net_cash_flow','mean'), op_cf=('operating_cash_flow','mean'),
    health=('overall_financial_health_score','mean'),
    current_ratio=('current_ratio','mean')).reset_index().sort_values('months_to_high', ascending=False)
print(cfm.round(0).to_string())

# DSO at T-1 and T-2 for each sub (2-3 month warning)
print("\n=== DSO at T-1, T-2, T-3 (for 2-3 month warning) ===")
for sub in d['subsidiary_id'].unique():
    s = d[d['subsidiary_id']==sub]
    vals = {}
    for mt in [3,2,1]:
        r = s[s['months_to_high']==mt]
        vals[mt] = round(r['weighted_average_days_outstanding'].iloc[0],1) if len(r) else 'NA'
    print(f"{sub}: DSO@T-3={vals[3]}, DSO@T-2={vals[2]}, DSO@T-1={vals[1]}, DSO@T0={round(s[s['months_to_high']==0]['weighted_average_days_outstanding'].iloc[0],1)}")
