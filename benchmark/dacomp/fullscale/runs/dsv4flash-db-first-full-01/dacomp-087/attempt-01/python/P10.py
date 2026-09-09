import json, pandas as pd, numpy as np

# Load data
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

# Build final portfolios
out_map = dict(zip(transfers_df['account_id'], transfers_df['from_owner']))
in_map = dict(zip(transfers_df['account_id'], transfers_df['to_owner']))

# For each rep, compute final portfolio
final_workloads = []
final_compliance = []
moved_accounts = set(transfers_df['account_id'])

for owner, grp in cust.groupby('owner_id'):
    # Remove transferred-out customers
    grp_out = grp[grp['account_id'].isin(moved_accounts) & grp['account_id'].isin(out_map) & (grp['owner_id'] == out_map[grp['account_id']]) if len(grp[grp['account_id'].isin(moved_accounts)]) > 0 else grp['owner_id'] == owner]
    # Actually simpler: remove any customer in moved set that was transferred FROM this owner
    removed = set()
    added = set()
    for acct in moved_accounts:
        if out_map.get(acct) == owner:
            removed.add(acct)
        if in_map.get(acct) == owner:
            added.add(acct)
    
    final_cust = grp[~grp['account_id'].isin(removed)]
    final_cust = pd.concat([final_cust, cust[cust['account_id'].isin(added)]])
    
    if len(final_cust) == 0:
        final_workloads.append({'owner_id': owner, 'workload': 0, 'n': 0})
        final_compliance.append({'owner_id': owner, 'pct_top3': 0})
        continue
    
    ws, cov = compute_workload(len(final_cust), final_cust['annual_revenue'].sum(),
                               final_cust['total_contacts'].sum(),
                               final_cust['billing_state'].nunique(),
                               final_cust['billing_city'].nunique())
    final_workloads.append({'owner_id': owner, 'workload': ws, 'n': len(final_cust), 'revenue': final_cust['annual_revenue'].sum()})
    
    top3 = final_cust['industry_normalized'].value_counts().head(3).index.tolist()
    pct = final_cust['industry_normalized'].isin(top3).mean()
    final_compliance.append({'owner_id': owner, 'pct_top3': pct, 'n': len(final_cust)})

fw = pd.DataFrame(final_workloads).set_index('owner_id')
fc = pd.DataFrame(final_compliance).set_index('owner_id')

print("===== FINAL WORKLOAD DISTRIBUTION =====")
print(f"Mean: {fw['workload'].mean():.4f}, Std: {fw['workload'].std():.4f}")
print(f"Min: {fw['workload'].min():.4f}, Max: {fw['workload'].max():.4f}")
print(f"Within ±15% of avg ({lower_target:.2f}-{upper_target:.2f}): {((fw['workload'] >= lower_target) & (fw['workload'] <= upper_target)).sum()} / {len(fw)}")
print(f"Below: {(fw['workload'] < lower_target).sum()}, Above: {(fw['workload'] > upper_target).sum()}")

print("\n===== BASELINE vs FINAL =====")
baseline_ws = rep_df.set_index('owner_id')['workload_score']
print(f"Baseline: Mean={baseline_ws.mean():.4f}, Std={baseline_ws.std():.4f}, in-range={((baseline_ws >= lower_target) & (baseline_ws <= upper_target)).sum()}/{len(baseline_ws)}")
print(f"Final:    Mean={fw['workload'].mean():.4f}, Std={fw['workload'].std():.4f}, in-range={((fw['workload'] >= lower_target) & (fw['workload'] <= upper_target)).sum()}/{len(fw)}")

print("\n===== INDUSTRY COMPLIANCE (≥60% in top 3) =====")
print(f"Baseline: {(baseline_ws.index.map(lambda o: fc.loc[o,'pct_top3'] if o in fc.index else 0) >= 0.6).sum() if False else 'see below'}")
# Recompute baseline compliance
baseline_compliance = []
for owner, grp in cust.groupby('owner_id'):
    top3 = grp['industry_normalized'].value_counts().head(3).index.tolist()
    baseline_compliance.append(grp['industry_normalized'].isin(top3).mean())
print(f"Baseline: {(np.array(baseline_compliance) >= 0.6).sum()} / 1000")
print(f"Final: {(fc['pct_top3'] >= 0.6).sum()} / {len(fc)}")
print(f"Final avg pct in top3: {fc['pct_top3'].mean():.4f}")

# Efficiency impact
print("\n===== EFFICIENCY IMPACT =====")
rep_eff = dict(zip(rep_df['owner_id'], rep_df['efficiency_score']))
team_eff_before = (rep_df['num_customers'] * rep_df['efficiency_score']).sum() / rep_df['num_customers'].sum()

# Total customers
total_cust = len(cust)
# Efficiency improvement: for each transfer, weight = 1/total_cust * (to_eff - from_eff)
improvement_equal = 0
improvement_rev = 0
total_rev = cust['annual_revenue'].sum()
for _, t in transfers_df.iterrows():
    from_eff = rep_eff.get(t['from_owner'], 0)
    to_eff = rep_eff.get(t['to_owner'], 0)
    improvement_equal += (1.0 / total_cust) * (to_eff - from_eff)
    improvement_rev += (t['revenue'] / total_rev) * (to_eff - from_eff)

print(f"Baseline team efficiency (customer-weighted): {team_eff_before:.4f}")
print(f"Expected improvement (equal weight): {improvement_equal:.4f}")
print(f"Team efficiency after (equal weight): {team_eff_before + improvement_equal:.4f} (+{improvement_equal/team_eff_before*100:.2f}%)")
print(f"Expected improvement (revenue-weighted): {improvement_rev:.4f}")
print(f"Team efficiency after (rev-weighted): {team_eff_before + improvement_rev:.4f} (+{improvement_rev/team_eff_before*100:.2f}%)")

# Retention impact
print("\n===== RETENTION IMPACT =====")
baseline_ret = 0.70
total_ret_imp = 0
for _, t in transfers_df.iterrows():
    improvement = 0.0
    to_owner = t['to_owner']
    # Industry match
    rec_cust = cust[cust['owner_id'] == to_owner]
    rec_cust = pd.concat([rec_cust, cust[cust['account_id'] == t['account_id']]])
    top3 = rec_cust['industry_normalized'].value_counts().head(3).index.tolist()
    if t['industry'] in top3:
        improvement += 0.05
    top_states = rec_cust['billing_state'].value_counts().head(3).index.tolist()
    if t['state'] in top_states:
        improvement += 0.05
    top_seg = rec_cust['account_size_segment'].value_counts().head(2).index.tolist()
    if t['segment'] in top_seg:
        improvement += 0.03
    total_ret_imp += improvement

avg_ret_imp = total_ret_imp / len(transfers_df)
print(f"Average retention improvement per transferred customer: {avg_ret_imp:.2%}")
print(f"Overall retention rate: {baseline_ret + avg_ret_imp:.2%} (from {baseline_ret:.0%})")

# Summary stats for report
print("\n===== TRANSFER SUMMARY =====")
print(f"Number of transfers: {len(transfers_df)}")
print(f"Number of unique donor reps: {transfers_df['from_owner'].nunique()}")
print(f"Number of unique receiver reps: {transfers_df['to_owner'].nunique()}")
print(f"Total revenue moved: ${transfers_df['revenue'].sum():,.0f}")
print(f"Avg revenue per transfer: ${transfers_df['revenue'].mean():,.0f}")
print(f"Avg donor workload reduction: {(transfers_df['donor_ws_before'] - transfers_df['donor_ws_after']).mean():.3f}")
print(f"Avg receiver workload increase: {(transfers_df['rec_ws_after'] - transfers_df['rec_ws_before']).mean():.3f}")

# State matching stats
same_state = transfers_df.apply(lambda r: cust[(cust['account_id']==r['account_id'])]['billing_state'].values[0] in set(cust[cust['owner_id']==r['to_owner']]['billing_state']), axis=1)
print(f"\nTransfers where customer state matches receiver's existing states: {same_state.sum()} / {len(transfers_df)}")

# Industry matching stats
ind_match = transfers_df.apply(lambda r: r['industry'] in set(cust[cust['owner_id']==r['to_owner']]['industry_normalized']), axis=1)
print(f"Transfers where customer industry matches receiver's existing industries: {ind_match.sum()} / {len(transfers_df)}")

# Save evaluation
fw.to_csv('/work/final_workloads.csv')
fc.to_csv('/work/final_compliance.csv')