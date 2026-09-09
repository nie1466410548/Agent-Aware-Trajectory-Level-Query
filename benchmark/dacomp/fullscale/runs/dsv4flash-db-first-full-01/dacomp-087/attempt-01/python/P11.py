import json, pandas as pd, numpy as np

rows = []
with open('/results/S19.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
rep_df = pd.DataFrame(rows)
rep_df.columns = ['owner_id', 'rep_name', 'manager_id', 'workload_score', 'efficiency_score',
                  'num_customers', 'total_annual_revenue', 'coverage_rate_capped',
                  'distinct_states', 'distinct_cities', 'win_rate', 'avg_deal_size_usd',
                  'avg_sales_cycle_days', 'opp_conversion_rate']
rep_df['efficiency_score'] = rep_df['efficiency_score'].fillna(rep_df['efficiency_score'].median())

cust = pd.read_csv('/work/customers.csv')
cust['account_id'] = cust['account_id'].astype(str)
transfers_df = pd.read_csv('/work/final_transfers.csv')
transfers_df['account_id'] = transfers_df['account_id'].astype(str)
transfers_df['revenue'] = pd.to_numeric(transfers_df['revenue'], errors='coerce')

def compute_workload(n_cust, total_rev, total_contacts, n_states, n_cities):
    if n_cust <= 0:
        return 0.0, 0.0
    coverage = min(5.0, total_contacts / n_cust)
    ws = n_cust * 0.3 + (total_rev / 1e6) / 10 * 0.4 + coverage * 0.2 + (n_states * 2.0 + n_cities * 0.5) * 0.1
    return ws, coverage

avg_ws = rep_df['workload_score'].mean()
lower_target = avg_ws * 0.85
upper_target = avg_ws * 1.15

out_map = dict(zip(transfers_df['account_id'], transfers_df['from_owner']))
in_map = dict(zip(transfers_df['account_id'], transfers_df['to_owner']))
moved = set(transfers_df['account_id'])

final_workloads = {}
final_compliance = {}

for owner, grp in cust.groupby('owner_id'):
    removed = {a for a in moved if out_map.get(a) == owner}
    added = {a for a in moved if in_map.get(a) == owner}
    final_cust = grp[~grp['account_id'].isin(removed)]
    if added:
        final_cust = pd.concat([final_cust, cust[cust['account_id'].isin(added)]])
    
    if len(final_cust) == 0:
        final_workloads[owner] = {'workload': 0.0, 'n': 0, 'revenue': 0}
        final_compliance[owner] = 0.0
        continue
    
    ws, cov = compute_workload(len(final_cust), final_cust['annual_revenue'].sum(),
                               final_cust['total_contacts'].sum(),
                               final_cust['billing_state'].nunique(),
                               final_cust['billing_city'].nunique())
    final_workloads[owner] = {'workload': ws, 'n': len(final_cust), 'revenue': final_cust['annual_revenue'].sum()}
    top3 = final_cust['industry_normalized'].value_counts().head(3).index.tolist()
    final_compliance[owner] = final_cust['industry_normalized'].isin(top3).mean()

fw = pd.DataFrame(final_workloads).T
baseline_ws = rep_df.set_index('owner_id')['workload_score']

print("===== WORKLOAD: BASELINE vs FINAL =====")
print(f"Baseline Mean={baseline_ws.mean():.4f} Std={baseline_ws.std():.4f} in-range={((baseline_ws>=lower_target)&(baseline_ws<=upper_target)).sum()}/1000")
print(f"Final    Mean={fw['workload'].mean():.4f} Std={fw['workload'].std():.4f} in-range={((fw['workload']>=lower_target)&(fw['workload']<=upper_target)).sum()}/{len(fw)}")
print(f"Final Min={fw['workload'].min():.4f} Max={fw['workload'].max():.4f}")

# Baseline compliance
base_comp = []
for owner, grp in cust.groupby('owner_id'):
    top3 = grp['industry_normalized'].value_counts().head(3).index.tolist()
    base_comp.append(grp['industry_normalized'].isin(top3).mean())
print("\n===== INDUSTRY COMPLIANCE (>=60% in top 3) =====")
print(f"Baseline: {(np.array(base_comp) >= 0.6).sum()}/1000 ({np.mean(base_comp):.3f} avg)")
fc = pd.Series(final_compliance)
print(f"Final:    {(fc >= 0.6).sum()}/{len(fc)} ({fc.mean():.3f} avg)")

# Efficiency impact
print("\n===== EFFICIENCY IMPACT =====")
rep_eff = dict(zip(rep_df['owner_id'], rep_df['efficiency_score']))
team_eff_before = (rep_df['num_customers'] * rep_df['efficiency_score']).sum() / rep_df['num_customers'].sum()
total_cust = len(cust)
total_rev = cust['annual_revenue'].sum()
imp_equal = 0.0
imp_rev = 0.0
for _, t in transfers_df.iterrows():
    fe = rep_eff.get(t['from_owner'], 0)
    te = rep_eff.get(t['to_owner'], 0)
    imp_equal += (1.0 / total_cust) * (te - fe)
    imp_rev += (t['revenue'] / total_rev) * (te - fe)
print(f"Baseline team efficiency: {team_eff_before:.4f}")
print(f"Equal-weight improvement: {imp_equal:.4f} -> {team_eff_before+imp_equal:.4f} (+{imp_equal/team_eff_before*100:.2f}%)")
print(f"Revenue-weighted improvement: {imp_rev:.4f} -> {team_eff_before+imp_rev:.4f} (+{imp_rev/team_eff_before*100:.2f}%)")

# Retention
print("\n===== RETENTION IMPACT =====")
baseline_ret = 0.70
total_ret_imp = 0.0
for _, t in transfers_df.iterrows():
    imp = 0.0
    rec_cust = cust[cust['owner_id'] == t['to_owner']]
    rec_cust = pd.concat([rec_cust, cust[cust['account_id'] == t['account_id']]])
    if t['industry'] in rec_cust['industry_normalized'].value_counts().head(3).index.tolist():
        imp += 0.05
    if t['state'] in rec_cust['billing_state'].value_counts().head(3).index.tolist():
        imp += 0.05
    if t['segment'] in rec_cust['account_size_segment'].value_counts().head(2).index.tolist():
        imp += 0.03
    total_ret_imp += imp
avg_ret_imp = total_ret_imp / len(transfers_df)
print(f"Avg retention improvement per transferred customer: {avg_ret_imp:.2%}")
print(f"Overall retention rate: {baseline_ret:.0%} -> {baseline_ret + avg_ret_imp:.2%}")

# Transfer stats
print("\n===== TRANSFER SUMMARY =====")
print(f"Transfers: {len(transfers_df)}")
print(f"Unique donors: {transfers_df['from_owner'].nunique()}, Unique receivers: {transfers_df['to_owner'].nunique()}")
print(f"Total revenue moved: ${transfers_df['revenue'].sum()/1e9:.2f}B")
print(f"Avg donor ws change: {(transfers_df['donor_ws_after']-transfers_df['donor_ws_before']).mean():.3f}")
print(f"Avg receiver ws change: {(transfers_df['rec_ws_after']-transfers_df['rec_ws_before']).mean():.3f}")

# Matching stats
def state_matches(r):
    return cust[cust['account_id']==r['account_id']]['billing_state'].values[0] in set(cust[cust['owner_id']==r['to_owner']]['billing_state'])
sm = transfers_df.apply(state_matches, axis=1)
print(f"Same-state matches: {sm.sum()}/{len(transfers_df)}")

def ind_matches(r):
    return r['industry'] in set(cust[cust['owner_id']==r['to_owner']]['industry_normalized'])
im = transfers_df.apply(ind_matches, axis=1)
print(f"Industry matches: {im.sum()}/{len(transfers_df)}")

# Save for visualization
fw.to_csv('/work/final_workloads.csv')
pd.Series(base_comp).to_csv('/work/baseline_compliance.csv')
fc.to_csv('/work/final_compliance_series.csv')