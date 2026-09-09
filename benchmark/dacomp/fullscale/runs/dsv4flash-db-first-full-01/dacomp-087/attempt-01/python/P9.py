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
cust['account_id'] = cust['account_id'].astype(str)

# Precompute per-owner data structures
owner_groups = {owner: grp for owner, grp in cust.groupby('owner_id')}
owner_industry_counts = {}
for owner, grp in cust.groupby('owner_id'):
    owner_industry_counts[owner] = grp['industry_normalized'].value_counts().to_dict()

def compute_workload(n_cust, total_rev, total_contacts, n_states, n_cities):
    if n_cust <= 0:
        return 0.0, 0.0
    coverage = min(5.0, total_contacts / n_cust)
    ws = n_cust * 0.3 + (total_rev / 1e6) / 10 * 0.4 + coverage * 0.2 + (n_states * 2.0 + n_cities * 0.5) * 0.1
    return ws, coverage

avg_ws = rep_df['workload_score'].mean()
lower_target = avg_ws * 0.85
upper_target = avg_ws * 1.15
print(f"Avg workload: {avg_ws:.4f}, Target range: [{lower_target:.4f}, {upper_target:.4f}]")

# Build current state
current = {}
for owner, grp in owner_groups.items():
    current[owner] = {
        'n_cust': len(grp),
        'total_rev': grp['annual_revenue'].sum(),
        'total_contacts': grp['total_contacts'].sum(),
        'states': grp['billing_state'].nunique(),
        'cities': grp['billing_city'].nunique(),
        'top3_industries': grp['industry_normalized'].value_counts().head(3).index.tolist(),
        'top_states': grp['billing_state'].value_counts().head(3).index.tolist(),
        'top_segments': grp['account_size_segment'].value_counts().head(2).index.tolist(),
    }

# Efficiency lookup
rep_eff = dict(zip(rep_df['owner_id'], rep_df['efficiency_score']))
rep_name = dict(zip(rep_df['owner_id'], rep_df['rep_name']))

donors = rep_df[rep_df['workload_score'] > upper_target].sort_values('workload_score', ascending=False)
receivers = rep_df[rep_df['workload_score'] < lower_target].sort_values('workload_score', ascending=True)
print(f"Donors: {len(donors)}, Receivers: {len(receivers)}")

# Receiver prefs
receiver_prefs = {}
for rid in receivers['owner_id'].tolist():
    exp = current[rid]
    receiver_prefs[rid] = {
        'pref_industries': set(exp['top3_industries']),
        'pref_states': set(exp['top_states']),
        'pref_segments': set(exp['top_segments']),
        'current_ws': rep_df[rep_df['owner_id'] == rid]['workload_score'].values[0],
    }

transfers = []

for _, donor in donors.iterrows():
    did = donor['owner_id']
    donor_exp = current[did]
    donor_cust = owner_groups[did]
    
    if len(donor_cust) == 0:
        continue
    
    # Score customers
    cust_scores = []
    state_counts = donor_cust['billing_state'].value_counts().to_dict()
    for _, c in donor_cust.iterrows():
        industry_score = 0 if c['industry_normalized'] in donor_exp['top3_industries'] else 10
        sc = state_counts.get(c['billing_state'], 1)
        state_score = 5.0 / sc
        rev_score = c['annual_revenue'] / 1e6 * 0.04
        cust_scores.append((c['account_id'], c['annual_revenue'], c['industry_normalized'],
                           c['billing_state'], c['account_size_segment'], industry_score + state_score + rev_score,
                           c['total_contacts']))
    cust_scores.sort(key=lambda x: x[5], reverse=True)
    
    cur_donor = current[did]
    cur_ws, _ = compute_workload(cur_donor['n_cust'], cur_donor['total_rev'],
                                  cur_donor['total_contacts'], cur_donor['states'], cur_donor['cities'])
    
    for acct_id, rev, ind, st, seg, score, contacts in cust_scores:
        if cur_ws <= upper_target:
            break
        
        best_rec = None
        best_match = -1e9
        
        for rid, prefs in receiver_prefs.items():
            rec_ws = prefs['current_ws']
            if rec_ws >= lower_target:
                continue
            
            match = 0
            if st in prefs['pref_states']:
                match += 100
            elif st in current[rid]['top_states']:
                match += 50
            
            if ind in prefs['pref_industries']:
                match += 80
            else:
                # check hypothetical top 3
                hyp = owner_industry_counts.get(rid, {}).copy()
                hyp[ind] = hyp.get(ind, 0) + 1
                sorted_hyp = sorted(hyp.items(), key=lambda x: x[1], reverse=True)
                top3_hyp = [h[0] for h in sorted_hyp[:3]]
                if ind in top3_hyp:
                    match += 40
            
            if seg in prefs['pref_segments']:
                match += 20
            
            capacity = lower_target - rec_ws
            match += capacity * 5
            match += rep_eff.get(rid, 0) * 10
            
            if match > best_match:
                best_match = match
                best_rec = rid
        
        if best_rec is None:
            continue
        
        # Check 60% rule for receiver
        rec_industries = owner_industry_counts.get(best_rec, {})
        total_rec = current[best_rec]['n_cust'] + 1
        hyp = rec_industries.copy()
        hyp[ind] = hyp.get(ind, 0) + 1
        sorted_hyp = sorted(hyp.items(), key=lambda x: x[1], reverse=True)
        top3_new = [h[0] for h in sorted_hyp[:3]]
        in_top3 = sum(v for k, v in hyp.items() if k in top3_new)
        pct_in_top3 = in_top3 / total_rec if total_rec > 0 else 0
        if pct_in_top3 < 0.60 and ind not in top3_new:
            continue
        
        # Workload impact
        new_donor_n = current[did]['n_cust'] - 1
        new_donor_rev = current[did]['total_rev'] - rev
        new_donor_contacts = current[did]['total_contacts'] - contacts
        if new_donor_n > 0:
            remaining = donor_cust[donor_cust['account_id'] != acct_id]
            new_donor_states = remaining['billing_state'].nunique()
            new_donor_cities = remaining['billing_city'].nunique()
        else:
            new_donor_states = 0; new_donor_cities = 0
        new_donor_ws, _ = compute_workload(new_donor_n, new_donor_rev, new_donor_contacts, new_donor_states, new_donor_cities)
        
        new_rec_n = current[best_rec]['n_cust'] + 1
        new_rec_rev = current[best_rec]['total_rev'] + rev
        new_rec_contacts = current[best_rec]['total_contacts'] + contacts
        # states/cities for receiver: approximate
        rec_states = current[best_rec]['states']
        rec_cities = current[best_rec]['cities']
        if st not in current[best_rec]['top_states']:
            rec_states += 1
        new_rec_ws, _ = compute_workload(new_rec_n, new_rec_rev, new_rec_contacts, rec_states, rec_cities)
        
        if new_rec_ws > upper_target:
            continue
        
        transfers.append({
            'from_owner': did, 'from_name': rep_name.get(did),
            'to_owner': best_rec, 'to_name': rep_name.get(best_rec),
            'account_id': acct_id, 'revenue': rev, 'industry': ind, 'state': st, 'segment': seg,
            'donor_ws_before': cur_ws, 'donor_ws_after': new_donor_ws,
            'rec_ws_before': receiver_prefs[best_rec]['current_ws'], 'rec_ws_after': new_rec_ws
        })
        
        # Update
        current[did]['n_cust'] = new_donor_n
        current[did]['total_rev'] = new_donor_rev
        current[did]['total_contacts'] = new_donor_contacts
        current[did]['states'] = new_donor_states
        current[did]['cities'] = new_donor_cities
        cur_ws = new_donor_ws
        # remove customer from donor group
        donor_cust = donor_cust[donor_cust['account_id'] != acct_id]
        
        current[best_rec]['n_cust'] = new_rec_n
        current[best_rec]['total_rev'] = new_rec_rev
        current[best_rec]['total_contacts'] = new_rec_contacts
        current[best_rec]['states'] = rec_states
        current[best_rec]['cities'] = rec_cities
        # update industry counts for receiver
        owner_industry_counts[best_rec][ind] = owner_industry_counts[best_rec].get(ind, 0) + 1
        # update prefs
        receiver_prefs[best_rec]['current_ws'] = new_rec_ws

transfers_df = pd.DataFrame(transfers)
print(f"\nTransfers proposed: {len(transfers_df)}")
print(f"Total revenue moved: ${transfers_df['revenue'].sum():,.0f}")
transfers_df.to_csv('/work/final_transfers.csv', index=False)
print(transfers_df[['from_name','to_name','revenue','industry','state','segment']].head(10).to_string())