import json, pandas as pd, numpy as np

# ---- Load data ----
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
# Ensure account_id is string
cust['account_id'] = cust['account_id'].astype(str)

# Check types
print("cust account_id dtype:", cust['account_id'].dtype)
print("sample account_id:", cust['account_id'].iloc[0])

# ---- Compute workload score for a portfolio ----
def compute_workload(n_cust, total_rev, total_contacts, n_states, n_cities):
    if n_cust <= 0:
        return 0, 0
    coverage = min(5.0, total_contacts / n_cust)
    ws = n_cust * 0.3 + (total_rev / 1e6) / 10 * 0.4 + coverage * 0.2 + (n_states * 2.0 + n_cities * 0.5) * 0.1
    return ws, coverage

# ---- Baseline metrics ----
avg_ws = rep_df['workload_score'].mean()
lower_target = avg_ws * 0.85
upper_target = avg_ws * 1.15
print(f"Avg workload: {avg_ws:.4f}, Target range: [{lower_target:.4f}, {upper_target:.4f}]")

# ---- Build rep expertise ----
rep_expertise = {}
for owner, grp in cust.groupby('owner_id'):
    top3_industries = grp['industry_normalized'].value_counts().head(3).index.tolist()
    top_states = grp['billing_state'].value_counts().head(3).index.tolist()
    top_segments = grp['account_size_segment'].value_counts().head(2).index.tolist()
    rep_expertise[owner] = {
        'top3_industries': top3_industries,
        'top_states': top_states,
        'top_segments': top_segments,
        'n_cust': len(grp),
        'total_rev': grp['annual_revenue'].sum(),
        'total_contacts': grp['total_contacts'].sum(),
        'states': grp['billing_state'].nunique(),
        'cities': grp['billing_city'].nunique(),
    }

# ---- Identify donors and receivers ----
donors = rep_df[rep_df['workload_score'] > upper_target].sort_values('workload_score', ascending=False)
receivers = rep_df[rep_df['workload_score'] < lower_target].sort_values('workload_score', ascending=True)
print(f"Donors: {len(donors)}, Receivers: {len(receivers)}, Stable: {len(rep_df) - len(donors) - len(receivers)}")

# ---- Reallocation algorithm ----
current = {owner: {k: v for k, v in exp.items()} for owner, exp in rep_expertise.items()}

# Pre-compute receiver preferences
receiver_prefs = {}
for _, rec in receivers.iterrows():
    rid = rec['owner_id']
    exp = current[rid]
    receiver_prefs[rid] = {
        'pref_industries': set(exp['top3_industries']),
        'pref_states': set(exp['top_states']),
        'pref_segments': set(exp['top_segments']),
        'current_ws': rec['workload_score'],
        'capacity': lower_target - rec['workload_score']
    }

transfers = []

for _, donor in donors.iterrows():
    did = donor['owner_id']
    donor_exp = current[did]
    donor_cust = cust[cust['owner_id'] == did].copy()
    
    if len(donor_cust) == 0:
        continue
    
    # Score customers for transfer-out suitability
    cust_scores = []
    for _, c in donor_cust.iterrows():
        industry_score = 0 if c['industry_normalized'] in donor_exp['top3_industries'] else 10
        state_count = len(donor_cust[donor_cust['billing_state'] == c['billing_state']])
        state_score = 5 / state_count if state_count > 0 else 0
        rev_score = c['annual_revenue'] / 1e6 * 0.04
        total_score = industry_score + state_score + rev_score
        cust_scores.append((c['account_id'], c['annual_revenue'], c['industry_normalized'], 
                           c['billing_state'], c['account_size_segment'], total_score, c['total_contacts']))
    
    cust_scores.sort(key=lambda x: x[5], reverse=True)
    
    # Current workload
    cur_donor = current[did]
    cur_ws, _ = compute_workload(cur_donor['n_cust'], cur_donor['total_rev'], 
                                  cur_donor['total_contacts'], cur_donor['states'], cur_donor['cities'])
    
    for acct_id, rev, ind, st, seg, score, contacts in cust_scores:
        if cur_ws <= upper_target:
            break
        
        # Find best receiver
        best_rec = None
        best_match = -1e9
        
        for rid, prefs in receiver_prefs.items():
            rec_ws = prefs['current_ws']
            if rec_ws >= lower_target:
                continue
            
            match = 0
            
            # Geographic proximity
            if st in prefs['pref_states']:
                match += 100
            elif st in current[rid]['top_states']:
                match += 50
            
            # Industry expertise
            if ind in prefs['pref_industries']:
                match += 80
            else:
                # Check if adding this customer would make it enter top 3
                hypothetical = cust[cust['owner_id'] == rid]['industry_normalized'].value_counts().to_dict()
                hypothetical[ind] = hypothetical.get(ind, 0) + 1
                hypothetical_sorted = sorted(hypothetical.items(), key=lambda x: x[1], reverse=True)
                top3_hyp = [h[0] for h in hypothetical_sorted[:3]]
                if ind in top3_hyp:
                    match += 40
            
            # Size suitability
            if seg in prefs['pref_segments']:
                match += 20
            
            # Room capacity
            capacity = lower_target - rec_ws
            match += capacity * 5
            
            # Efficiency potential
            rec_eff = rep_df[rep_df['owner_id'] == rid]['efficiency_score'].values[0]
            match += rec_eff * 10
            
            if match > best_match:
                best_match = match
                best_rec = rid
        
        if best_rec is None:
            continue
        
        # Check 60% industry rule for receiver
        rec_cust = cust[cust['owner_id'] == best_rec]
        industries = rec_cust['industry_normalized'].tolist() + [ind]
        top3_new = pd.Series(industries).value_counts().head(3).index.tolist()
        pct_in_top3 = pd.Series(industries).isin(top3_new).mean()
        
        if pct_in_top3 < 0.60 and ind not in top3_new:
            continue
        
        # Compute workload impact
        new_donor_n = current[did]['n_cust'] - 1
        new_donor_rev = current[did]['total_rev'] - rev
        new_donor_contacts = current[did]['total_contacts'] - contacts
        
        if new_donor_n > 0:
            remaining = cust[(cust['owner_id'] == did) & (cust['account_id'] != acct_id)]
            new_donor_states = remaining['billing_state'].nunique()
            new_donor_cities = remaining['billing_city'].nunique()
        else:
            new_donor_states = 0
            new_donor_cities = 0
        
        new_donor_ws, _ = compute_workload(new_donor_n, new_donor_rev, new_donor_contacts, 
                                            new_donor_states, new_donor_cities)
        
        new_rec_n = current[best_rec]['n_cust'] + 1
        new_rec_rev = current[best_rec]['total_rev'] + rev
        new_rec_contacts = current[best_rec]['total_contacts'] + contacts
        
        # Recompute states/cities for receiver
        rec_plus = cust[(cust['owner_id'] == best_rec)]
        rec_plus = pd.concat([rec_plus, cust[cust['account_id'] == acct_id]])
        new_rec_states = rec_plus['billing_state'].nunique()
        new_rec_cities = rec_plus['billing_city'].nunique()
        
        new_rec_ws, _ = compute_workload(new_rec_n, new_rec_rev, new_rec_contacts, 
                                          new_rec_states, new_rec_cities)
        
        if new_rec_ws > upper_target:
            continue
        
        # Record transfer
        rec_name = rep_df[rep_df['owner_id'] == best_rec]['rep_name'].values[0]
        transfers.append({
            'from_owner': did,
            'from_name': donor['rep_name'],
            'to_owner': best_rec,
            'to_name': rec_name,
            'account_id': acct_id,
            'revenue': rev,
            'industry': ind,
            'state': st,
            'segment': seg,
            'donor_ws_before': cur_ws,
            'donor_ws_after': new_donor_ws,
            'rec_ws_before': receiver_prefs[best_rec]['current_ws'],
            'rec_ws_after': new_rec_ws
        })
        
        # Update state
        current[did]['n_cust'] = new_donor_n
        current[did]['total_rev'] = new_donor_rev
        current[did]['total_contacts'] = new_donor_contacts
        current[did]['states'] = new_donor_states
        current[did]['cities'] = new_donor_cities
        cur_ws = new_donor_ws
        
        current[best_rec]['n_cust'] = new_rec_n
        current[best_rec]['total_rev'] = new_rec_rev
        current[best_rec]['total_contacts'] = new_rec_contacts
        current[best_rec]['states'] = new_rec_states
        current[best_rec]['cities'] = new_rec_cities
        
        # Update receiver prefs
        if best_rec in receiver_prefs:
            receiver_prefs[best_rec]['current_ws'] = new_rec_ws
            receiver_prefs[best_rec]['capacity'] = lower_target - new_rec_ws

transfers_df = pd.DataFrame(transfers)
print(f"\nTransfers proposed: {len(transfers_df)}")
print(f"Total revenue moved: ${transfers_df['revenue'].sum():,.0f}")

# ---- Evaluate final state ----
final_workloads = {}
final_compliance = {}
for owner in current:
    exp = current[owner]
    ws, _ = compute_workload(exp['n_cust'], exp['total_rev'], exp['total_contacts'], exp['states'], exp['cities'])
    final_workloads[owner] = ws
    
    # Final customer portfolio
    actual_cust = cust[cust['owner_id'] == owner]
    if len(transfers_df) > 0:
        transferred_in = transfers_df[transfers_df['to_owner'] == owner]['account_id'].tolist()
        transferred_out = transfers_df[transfers_df['from_owner'] == owner]['account_id'].tolist()
        actual_cust = actual_cust[~actual_cust['account_id'].isin(transferred_out)]
        actual_cust = pd.concat([actual_cust, cust[cust['account_id'].isin(transferred_in)]])
    
    if len(actual_cust) > 0:
        top3 = actual_cust['industry_normalized'].value_counts().head(3).index.tolist()
        pct = actual_cust['industry_normalized'].isin(top3).mean()
        final_compliance[owner] = pct
    else:
        final_compliance[owner] = 0

final_ws_series = pd.Series(final_workloads)
print(f"\nFinal workload stats:")
print(f"Mean: {final_ws_series.mean():.4f}, Std: {final_ws_series.std():.4f}")
print(f"Min: {final_ws_series.min():.4f}, Max: {final_ws_series.max():.4f}")
print(f"Within ±15% range: {((final_ws_series >= lower_target) & (final_ws_series <= upper_target)).sum()} / {len(final_ws_series)}")
print(f"Below: {(final_ws_series < lower_target).sum()}, Above: {(final_ws_series > upper_target).sum()}")

comp_series = pd.Series(final_compliance)
print(f"\nFinal industry compliance (≥60% in top 3): {(comp_series >= 0.6).sum()} / {len(comp_series)} ({comp_series.mean():.1%} avg)")

# ---- Efficiency impact ----
total_cust_count = cust['owner_id'].value_counts()
team_eff_before = 0
for owner_id, cnt in total_cust_count.items():
    eff = rep_df[rep_df['owner_id'] == owner_id]['efficiency_score'].values[0]
    team_eff_before += cnt * eff
team_eff_before /= total_cust_count.sum()
print(f"\nBaseline team efficiency (customer-weighted): {team_eff_before:.4f}")

# Compute impact
total_improvement = 0
total_cust_after = total_cust_count.sum()
for _, t in transfers_df.iterrows():
    from_eff = rep_df[rep_df['owner_id'] == t['from_owner']]['efficiency_score'].values[0]
    to_eff = rep_df[rep_df['owner_id'] == t['to_owner']]['efficiency_score'].values[0]
    total_improvement += (1.0 / total_cust_after) * (to_eff - from_eff)

print(f"Efficiency improvement (equal weight): {total_improvement:.4f}")
print(f"Team efficiency after: {team_eff_before + total_improvement:.4f}")
print(f"Improvement %: {total_improvement / team_eff_before * 100:.2f}%")

# Revenue-weighted
total_rev = cust['annual_revenue'].sum()
rev_weighted = 0
for _, t in transfers_df.iterrows():
    from_eff = rep_df[rep_df['owner_id'] == t['from_owner']]['efficiency_score'].values[0]
    to_eff = rep_df[rep_df['owner_id'] == t['to_owner']]['efficiency_score'].values[0]
    rev_weighted += (t['revenue'] / total_rev) * (to_eff - from_eff)
print(f"Revenue-weighted efficiency improvement: {rev_weighted:.4f}")

# ---- Retention probability ----
baseline_ret = 0.70
total_ret_improvement = 0
for _, t in transfers_df.iterrows():
    improvement = 0
    to_owner = t['to_owner']
    rec_cust = cust[cust['owner_id'] == to_owner]
    rec_cust = pd.concat([rec_cust, cust[cust['account_id'] == t['account_id']]])
    top3 = rec_cust['industry_normalized'].value_counts().head(3).index.tolist()
    if t['industry'] in top3:
        improvement += 0.05
    if t['state'] in rec_cust['billing_state'].value_counts().head(3).index.tolist():
        improvement += 0.05
    rec_segments = rec_cust['account_size_segment'].value_counts().head(2).index.tolist()
    if t['segment'] in rec_segments:
        improvement += 0.03
    total_ret_improvement += improvement

avg_ret_improvement = total_ret_improvement / len(transfers_df) if len(transfers_df) > 0 else 0
print(f"\nAverage retention improvement per transfer: {avg_ret_improvement:.2%}")
print(f"Overall expected retention rate: {baseline_ret + avg_ret_improvement:.2%}")

# Save
transfers_df.to_csv('/work/final_transfers.csv', index=False)

# Print sample
print(f"\n===== SAMPLE TRANSFERS (first 10) =====")
cols = ['from_name', 'to_name', 'revenue', 'industry', 'state', 'segment', 'donor_ws_before', 'donor_ws_after', 'rec_ws_before', 'rec_ws_after']
print(transfers_df[cols].head(10).to_string())