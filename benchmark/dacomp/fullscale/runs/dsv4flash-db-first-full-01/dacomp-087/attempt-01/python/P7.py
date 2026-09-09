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

# ---- Compute workload score for a portfolio ----
def compute_workload(n_cust, total_rev, total_contacts, n_states, n_cities):
    coverage = min(5.0, total_contacts / n_cust) if n_cust > 0 else 0
    ws = n_cust * 0.3 + (total_rev / 1e6) / 10 * 0.4 + coverage * 0.2 + (n_states * 2.0 + n_cities * 0.5) * 0.1
    return ws, coverage

# ---- Baseline metrics ----
avg_ws = rep_df['workload_score'].mean()
lower_target = avg_ws * 0.85
upper_target = avg_ws * 1.15
print(f"Avg workload: {avg_ws:.4f}, Target range: [{lower_target:.4f}, {upper_target:.4f}]")

# ---- Compute baseline industry compliance ----
def get_top3_compliance(cust_df, owner_id):
    """Return (pct_in_top3, top3_industries)"""
    grp = cust_df[cust_df['owner_id'] == owner_id]
    if len(grp) == 0:
        return 0.0, []
    top3 = grp['industry_normalized'].value_counts().head(3).index.tolist()
    pct = grp['industry_normalized'].isin(top3).mean()
    return pct, top3

# ---- Build state-industry-size expertise for each rep ----
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
        'pct_top3': get_top3_compliance(cust, owner)[0]
    }

print(f"Baseline: {(sum(1 for v in rep_expertise.values() if v['pct_top3'] >= 0.6))} reps meet 60% industry rule")

# ---- Identify donors (overloaded) and receivers (underloaded) ----
# We'll work with the actual workload scores
donors = rep_df[rep_df['workload_score'] > upper_target].sort_values('workload_score', ascending=False)
receivers = rep_df[rep_df['workload_score'] < lower_target].sort_values('workload_score', ascending=True)

print(f"Donors: {len(donors)}, Receivers: {len(receivers)}, Stable: {len(rep_df) - len(donors) - len(receivers)}")

# ---- Reallocation algorithm ----
# For each donor, we'll try to transfer customers out
# Priority: customers not in donor's top 3 industries (improves their compliance)
# Then customers in states that are rare for the donor (reduces geo complexity)

transfers = []  # (from_owner, to_owner, account_id, revenue, industry, state, size)

# Track current state
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
        'capacity': lower_target - rec['workload_score']  # how much room
    }

# Iterate donors
for _, donor in donors.iterrows():
    did = donor['owner_id']
    donor_exp = current[did]
    donor_cust = cust[cust['owner_id'] == did].copy()
    
    # Score each customer for transfer-out suitability
    # Higher score = better to transfer out
    cust_scores = []
    for _, c in donor_cust.iterrows():
        # Score based on:
        # 1. Not in top 3 industries of donor (improves compliance)
        industry_score = 0 if c['industry_normalized'] in donor_exp['top3_industries'] else 10
        # 2. State rarity: if state has few customers, transfer reduces geo complexity
        state_count = len(donor_cust[donor_cust['billing_state'] == c['billing_state']])
        state_score = 5 / state_count  # Rarer state = higher score
        # 3. Revenue contribution (transferring high revenue reduces workload more)
        rev_score = c['annual_revenue'] / 1e6 * 0.04  # This is the revenue term in workload
        # Total score
        total_score = industry_score + state_score + rev_score
        cust_scores.append((c['account_id'], c['annual_revenue'], c['industry_normalized'], 
                           c['billing_state'], c['account_size_segment'], total_score,
                           c['total_contacts']))
    
    cust_scores.sort(key=lambda x: x[5], reverse=True)
    
    # What's the current workload of the donor?
    # Recompute from current state
    cur_donor = current[did]
    cur_ws, _ = compute_workload(cur_donor['n_cust'], cur_donor['total_rev'], 
                                  cur_donor['total_contacts'], cur_donor['states'], cur_donor['cities'])
    
    for acct_id, rev, ind, st, seg, score, contacts in cust_scores:
        if cur_ws <= upper_target:
            break
        
        # Find best receiver for this customer
        best_rec = None
        best_match = -1e9
        
        for rid, prefs in receiver_prefs.items():
            rec_ws = prefs['current_ws']
            if rec_ws >= lower_target:
                continue
            
            # Match score
            match = 0
            
            # 1. Geographic proximity: same state is highly preferred
            if st in prefs['pref_states']:
                match += 100
            elif st in current[rid]['states']:
                match += 50
            
            # 2. Industry expertise match: prefer if industry in top 3
            if ind in prefs['pref_industries']:
                match += 80
            else:
                # Check if adding this customer would make it enter top 3
                hypothetical = cust[cust['owner_id'] == rid]['industry_normalized'].value_counts()
                hypothetical = hypothetical.to_dict()
                hypothetical[ind] = hypothetical.get(ind, 0) + 1
                hypothetical_sorted = sorted(hypothetical.items(), key=lambda x: x[1], reverse=True)
                top3_hyp = [h[0] for h in hypothetical_sorted[:3]]
                if ind in top3_hyp:
                    match += 40
            
            # 3. Size suitability
            if seg in prefs['pref_segments']:
                match += 20
            
            # 4. Room capacity
            capacity = lower_target - rec_ws
            match += capacity * 5
            
            # 5. Efficiency improvement potential (prefer receivers with higher efficiency)
            rec_eff = rep_df[rep_df['owner_id'] == rid]['efficiency_score'].values[0]
            match += rec_eff * 10
            
            if match > best_match:
                best_match = match
                best_rec = rid
        
        if best_rec is None:
            continue
        
        # Check if this transfer would violate the 60% industry rule for the receiver
        rec_cust = cust[cust['owner_id'] == best_rec]
        # Simulate adding this customer
        industries = rec_cust['industry_normalized'].tolist() + [ind]
        top3_new = pd.Series(industries).value_counts().head(3).index.tolist()
        pct_in_top3 = pd.Series(industries).isin(top3_new).mean()
        
        # If below 60% AND the new customer's industry is NOT in the top 3, skip
        # (If it IS in top 3, then compliance is maintained or improved)
        if pct_in_top3 < 0.60 and ind not in top3_new:
            continue
        
        # Compute the workload impact of this transfer
        # Donor loses this customer
        new_donor_n = current[did]['n_cust'] - 1
        new_donor_rev = current[did]['total_rev'] - rev
        new_donor_contacts = current[did]['total_contacts'] - contacts
        
        # Recompute states/cities for donor
        if new_donor_n > 0:
            remaining = cust[(cust['owner_id'] == did) & (cust['account_id'] != acct_id)]
            new_donor_states = remaining['billing_state'].nunique()
            new_donor_cities = remaining['billing_city'].nunique()
        else:
            new_donor_states = 0
            new_donor_cities = 0
        
        new_donor_ws, _ = compute_workload(new_donor_n, new_donor_rev, new_donor_contacts, 
                                            new_donor_states, new_donor_cities)
        
        # Receiver gains this customer
        new_rec_n = current[best_rec]['n_cust'] + 1
        new_rec_rev = current[best_rec]['total_rev'] + rev
        new_rec_contacts = current[best_rec]['total_contacts'] + contacts
        
        rec_plus = cust[(cust['owner_id'] == best_rec)]
        rec_plus = pd.concat([rec_plus, cust[cust['account_id'] == acct_id]])
        new_rec_states = rec_plus['billing_state'].nunique()
        new_rec_cities = rec_plus['billing_city'].nunique()
        
        new_rec_ws, _ = compute_workload(new_rec_n, new_rec_rev, new_rec_contacts, 
                                          new_rec_states, new_rec_cities)
        
        # Check that receiver's workload doesn't exceed upper bound
        if new_rec_ws > upper_target:
            continue
        
        # Record transfer
        transfers.append({
            'from_owner': did,
            'from_name': donor['rep_name'],
            'to_owner': best_rec,
            'to_name': rep_df[rep_df['owner_id'] == best_rec]['rep_name'].values[0],
            'account_id': acct_id,
            'revenue': rev,
            'industry': ind,
            'state': st,
            'segment': seg,
            'donor_ws_before': cur_ws,
            'donor_ws_after': new_donor_ws,
            'rec_ws_before': prefs['current_ws'] if best_rec in receiver_prefs else receiver_prefs.get(best_rec, {}).get('current_ws', 0),
            'rec_ws_after': new_rec_ws
        })
        
        # Update current state
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
# Recompute all workload scores
final_workloads = {}
final_compliance = {}
for owner, exp in current.items():
    ws, _ = compute_workload(exp['n_cust'], exp['total_rev'], exp['total_contacts'], exp['states'], exp['cities'])
    final_workloads[owner] = ws
    
    # Recompute compliance
    actual_cust = cust[cust['owner_id'] == owner]
    if len(transfers_df) > 0:
        # Add transferred-in customers
        transferred_in = transfers_df[transfers_df['to_owner'] == owner]['account_id'].tolist()
        # Remove transferred-out customers
        transferred_out = transfers_df[transfers_df['from_owner'] == owner]['account_id'].tolist()
        actual_cust = actual_cust[~actual_cust['account_id'].isin(transferred_out)]
        actual_cust = pd.concat([actual_cust, cust[cust['account_id'].isin(transferred_in)]])
    
    if len(actual_cust) > 0:
        top3 = actual_cust['industry_normalized'].value_counts().head(3).index.tolist()
        pct = actual_cust['industry_normalized'].isin(top3).mean()
        final_compliance[owner] = pct
    else:
        final_compliance[owner] = 0

# Results
final_ws_series = pd.Series(final_workloads)
print(f"\nFinal workload stats:")
print(f"Mean: {final_ws_series.mean():.4f}, Std: {final_ws_series.std():.4f}")
print(f"Min: {final_ws_series.min():.4f}, Max: {final_ws_series.max():.4f}")
print(f"Within ±15% range: {((final_ws_series >= lower_target) & (final_ws_series <= upper_target)).sum()} / {len(final_ws_series)}")
print(f"Below lower bound: {(final_ws_series < lower_target).sum()}")
print(f"Above upper bound: {(final_ws_series > upper_target).sum()}")

# Compliance
comp_series = pd.Series(final_compliance)
print(f"\nFinal compliance with 60% industry rule:")
print(f"Mean: {comp_series.mean():.4f}")
print(f"Meeting 60%: {(comp_series >= 0.6).sum()} / {len(comp_series)}")

# ---- Compute efficiency impact ----
# For each transferred customer, estimate the expected improvement
# in efficiency score. The team efficiency is a weighted average.
# We'll use the rep's efficiency score as a proxy for expected value generation.

# Baseline team efficiency (weighted by customer count)
total_cust = cust['owner_id'].value_counts()
team_eff_before = 0
for owner_id, cnt in total_cust.items():
    eff = rep_df[rep_df['owner_id'] == owner_id]['efficiency_score'].values[0]
    team_eff_before += cnt * eff
team_eff_before /= total_cust.sum()
print(f"\nBaseline team efficiency (customer-weighted): {team_eff_before:.4f}")

# After reallocation: compute expected efficiency
# For each rep, we estimate their efficiency score based on their portfolio
# Actually, efficiency score is a property of the rep, not the portfolio.
# But we can estimate the expected value generated per customer.

# A simpler approach: the expected improvement from moving a customer
# from rep A to rep B is proportional to (eff_B - eff_A) * customer_weight

# Let's compute the total expected improvement
total_improvement = 0
total_cust_after = total_cust.sum()  # Same total customers

for _, t in transfers_df.iterrows():
    from_eff = rep_df[rep_df['owner_id'] == t['from_owner']]['efficiency_score'].values[0]
    to_eff = rep_df[rep_df['owner_id'] == t['to_owner']]['efficiency_score'].values[0]
    # Customer weight = 1 / total_cust (equal weight)
    # Or weight by revenue
    weight = 1.0 / total_cust_after
    total_improvement += weight * (to_eff - from_eff)

print(f"Total expected efficiency improvement (equal weight): {total_improvement:.4f}")
print(f"Team efficiency after: {team_eff_before + total_improvement:.4f}")
print(f"Improvement %: {total_improvement / team_eff_before * 100:.2f}%")

# Revenue-weighted improvement
total_rev = cust['annual_revenue'].sum()
rev_weighted_improvement = 0
for _, t in transfers_df.iterrows():
    from_eff = rep_df[rep_df['owner_id'] == t['from_owner']]['efficiency_score'].values[0]
    to_eff = rep_df[rep_df['owner_id'] == t['to_owner']]['efficiency_score'].values[0]
    weight = t['revenue'] / total_rev
    rev_weighted_improvement += weight * (to_eff - from_eff)

print(f"Revenue-weighted efficiency improvement: {rev_weighted_improvement:.4f}")
print(f"Revenue-weighted team efficiency after: {team_eff_before + rev_weighted_improvement:.4f}")

# ---- Retention probability impact ----
# We estimate retention probability improves when:
# - Customer is matched to a rep with industry expertise
# - Customer is in the same state as the rep's other customers
# Baseline retention: 70%
# Improvement: 5% for industry match, 5% for state match, 3% for size match

baseline_retention = 0.70
total_ret_improvement = 0
for _, t in transfers_df.iterrows():
    improvement = 0
    # Check if industry is in receiver's top 3 (post-transfer)
    to_owner = t['to_owner']
    rec_cust = cust[cust['owner_id'] == to_owner]
    rec_cust = pd.concat([rec_cust, cust[cust['account_id'] == t['account_id']]])
    top3 = rec_cust['industry_normalized'].value_counts().head(3).index.tolist()
    if t['industry'] in top3:
        improvement += 0.05
    # Check state match
    if t['state'] in rec_cust['billing_state'].value_counts().head(3).index.tolist():
        improvement += 0.05
    # Check size match
    rec_segments = rec_cust['account_size_segment'].value_counts().head(2).index.tolist()
    if t['segment'] in rec_segments:
        improvement += 0.03
    
    total_ret_improvement += improvement * (1.0 / len(transfers_df))

avg_ret_improvement = total_ret_improvement
print(f"\nAverage retention probability improvement per transfer: {avg_ret_improvement:.2%}")
print(f"Overall retention rate improvement: {avg_ret_improvement * 100:.2f} percentage points")

# Save results
transfers_df.to_csv('/work/final_transfers.csv', index=False)

# Print sample transfers
print(f"\n===== SAMPLE TRANSFERS (first 10) =====")
cols = ['from_name', 'to_name', 'account_id', 'revenue', 'industry', 'state', 'segment']
print(transfers_df[cols].head(10).to_string())

# Also print the top 5 donors and receivers
print(f"\nTop 5 Donors (most overloaded):")
print(rep_df[rep_df['owner_id'].isin(transfers_df['from_owner'].unique())].head(5)[['rep_name', 'workload_score', 'efficiency_score']].to_string())

print(f"\nTop 5 Receivers (most underloaded):")
print(rep_df[rep_df['owner_id'].isin(transfers_df['to_owner'].unique())].head(5)[['rep_name', 'workload_score', 'efficiency_score']].to_string())