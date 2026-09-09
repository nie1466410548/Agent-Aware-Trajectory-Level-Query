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

cust = pd.read_csv('/work/customers.csv')

# Fill NaN efficiency scores with median
median_eff = rep_df['efficiency_score'].median()
rep_df['efficiency_score'] = rep_df['efficiency_score'].fillna(median_eff)

# ---- Step 1: Compute workload stats ----
avg_ws = rep_df['workload_score'].mean()
std_ws = rep_df['workload_score'].std()
print(f"Avg workload: {avg_ws:.4f}, Std: {std_ws:.4f}")
print(f"Threshold (std > 0.3*avg): {std_ws:.4f} > {0.3*avg_ws:.4f}: {std_ws > 0.3*avg_ws}")

# Target range: ±15% of average
lower_bound = avg_ws * 0.85
upper_bound = avg_ws * 1.15
print(f"Target workload range: [{lower_bound:.4f}, {upper_bound:.4f}]")

# Identify donors (above range) and receivers (below range)
donors = rep_df[rep_df['workload_score'] > upper_bound].copy()
receivers = rep_df[rep_df['workload_score'] < lower_bound].copy()
stable = rep_df[(rep_df['workload_score'] >= lower_bound) & (rep_df['workload_score'] <= upper_bound)]

print(f"\nDonors (overloaded): {len(donors)}")
print(f"Receivers (underloaded): {len(receivers)}")
print(f"Stable: {len(stable)}")

# ---- Step 2: For each rep, compute their top 3 industries and state distribution ----
# Top industries per rep
rep_industries = cust.groupby('owner_id')['industry_normalized'].apply(
    lambda x: x.value_counts().head(3).index.tolist()
).to_dict()

# States per rep
rep_states = cust.groupby('owner_id')['billing_state'].apply(list).to_dict()
rep_primary_states = cust.groupby('owner_id')['billing_state'].apply(
    lambda x: x.value_counts().index.tolist()
).to_dict()

# Account size segments per rep
rep_segments = cust.groupby('owner_id')['account_size_segment'].apply(
    lambda x: x.value_counts().index.tolist()
).to_dict()

# ---- Step 3: For each donor, identify customers that could be transferred ----
# Sort customers by contribution to workload (revenue is the dominant factor)
# The workload contribution of a customer to the rep's workload is roughly:
# revenue_contrib = (annual_revenue / 1e6) / 10 * 0.4 = annual_revenue * 0.04 / 1e6

# For each donor, compute the "transfer-out value" for each customer
# We'll consider: high revenue customers are good to transfer out (reduces workload more)
# Also geographic complexity: if a customer is in a state with few other customers, it contributes to geo complexity

def compute_transfer_candidates(donor_id, donor_df, cust_df, rep_states_dict, rep_industries_dict):
    """Compute which customers could be transferred from this donor."""
    donor_cust = cust_df[cust_df['owner_id'] == donor_id].copy()
    if len(donor_cust) == 0:
        return []
    
    donor_state_list = rep_states_dict.get(donor_id, [])
    donor_industry_list = rep_industries_dict.get(donor_id, [])
    
    # For each customer, compute:
    # 1. Revenue contribution to workload: annual_revenue * 0.04 / 1e6
    # 2. State uniqueness: how many other customers in that state
    state_counts = donor_cust['billing_state'].value_counts()
    
    donor_cust['revenue_ws_contrib'] = donor_cust['annual_revenue'] * 0.04 / 1e6
    donor_cust['state_count'] = donor_cust['billing_state'].map(state_counts)
    donor_cust['transfer_score'] = donor_cust['revenue_ws_contrib'] / donor_cust['state_count']
    
    # Sort by transfer priority (high revenue, rare state)
    donor_cust = donor_cust.sort_values('transfer_score', ascending=False)
    return donor_cust

# For each receiver, compute which types of customers they'd prefer
def compute_receiver_preferences(receiver_id, cust_df, rep_industries_dict, rep_states_dict, rep_segments_dict):
    """Compute preferences for a receiver."""
    # Preferred industries (top 3)
    pref_industries = rep_industries_dict.get(receiver_id, [])
    # Preferred states (where they already have customers)
    pref_states = rep_states_dict.get(receiver_id, [])
    # Preferred segments
    pref_segments = rep_segments_dict.get(receiver_id, [])
    return pref_industries, pref_states, pref_segments

# Let's create a matching algorithm
# We'll iterate donors in descending order of workload (highest first)
# For each donor, find candidate customers to transfer
# For each candidate, find the best receiver (matching industry, state, size)

donors_sorted = donors.sort_values('workload_score', ascending=False)
receivers_sorted = receivers.sort_values('workload_score', ascending=True)

# Proposed transfers list
transfers = []  # list of (from_owner, to_owner, account_id, account_name, annual_revenue)

# Track updated workload scores (simulate transfers)
updated_ws = rep_df[['owner_id', 'workload_score', 'num_customers', 'total_annual_revenue', 
                      'distinct_states', 'distinct_cities', 'coverage_rate_capped']].copy()
updated_ws = updated_ws.set_index('owner_id')

# For each donor, try to transfer out customers
for idx, donor_row in donors_sorted.iterrows():
    donor_id = donor_row['owner_id']
    donor_ws = updated_ws.loc[donor_id, 'workload_score']
    
    if donor_ws <= upper_bound:
        continue
    
    donor_cust = compute_transfer_candidates(donor_id, donor_row, cust, rep_states, rep_industries)
    
    for cust_idx, cust_row in donor_cust.iterrows():
        if donor_ws <= upper_bound:
            break
        
        # Find best receiver for this customer
        best_receiver = None
        best_score = -1e9
        
        for ridx, rec_row in receivers_sorted.iterrows():
            receiver_id = rec_row['owner_id']
            rec_ws = updated_ws.loc[receiver_id, 'workload_score']
            
            if rec_ws >= lower_bound:
                continue
            
            pref_industries, pref_states, pref_segments = compute_receiver_preferences(
                receiver_id, cust, rep_industries, rep_states, rep_segments
            )
            
            # Compute match score
            match_score = 0
            
            # Geographic proximity: same state is best
            if cust_row['billing_state'] in pref_states:
                match_score += 100
            else:
                # Penalize different state
                match_score -= 10
            
            # Industry expertise match: at least 60% of rep's customers should be in top 3 industries
            if cust_row['industry_normalized'] in pref_industries:
                match_score += 50
            else:
                match_score -= 20
            
            # Size suitability
            if cust_row['account_size_segment'] in rep_segments.get(receiver_id, []):
                match_score += 20
            
            # Prefer receivers with lower workload (more room)
            match_score += (lower_bound - rec_ws) * 2
            
            if match_score > best_score:
                best_score = match_score
                best_receiver = receiver_id
        
        if best_receiver is None:
            continue
        
        # Check if moving this customer would make the receiver's industry match < 60%
        # Compute what receiver's top 3 industries would be after addition
        receiver_cust = cust[cust['owner_id'] == best_receiver]
        hypothetical_industries = pd.concat([
            receiver_cust['industry_normalized'],
            pd.Series([cust_row['industry_normalized']])
        ]).value_counts()
        
        # Check if the new customer's industry is in the top 3
        top3_after = hypothetical_industries.head(3).index.tolist()
        if cust_row['industry_normalized'] not in top3_after:
            # Check if the receiver would still have at least 60% in top 3
            total_after = len(receiver_cust) + 1
            in_top3_after = hypothetical_industries[hypothetical_industries.index.isin(top3_after)].sum()
            pct_in_top3 = in_top3_after / total_after
            if pct_in_top3 < 0.6:
                continue  # Skip this transfer to maintain 60% rule
        
        # Simulate the transfer
        # Update workload for donor
        # Revenue contribution removed
        new_rev_donor = updated_ws.loc[donor_id, 'total_annual_revenue'] - cust_row['annual_revenue']
        new_cust_donor = updated_ws.loc[donor_id, 'num_customers'] - 1
        new_contacts_donor = updated_ws.loc[donor_id, 'coverage_rate_capped'] * (updated_ws.loc[donor_id, 'num_customers']) - cust_row['total_contacts']
        # Actually, coverage_rate_capped is contacts/customers capped at 5
        # We need to recompute properly
        
        # Recompute for donor
        old_cust_donor = updated_ws.loc[donor_id, 'num_customers']
        old_rev_donor = updated_ws.loc[donor_id, 'total_annual_revenue']
        old_contacts_donor = old_cust_donor * updated_ws.loc[donor_id, 'coverage_rate_capped']
        new_contacts_donor = max(0, old_contacts_donor - cust_row['total_contacts'])
        new_cust_donor = old_cust_donor - 1
        new_cov_donor = min(5.0, new_contacts_donor / new_cust_donor) if new_cust_donor > 0 else 0
        
        # Update distinct states & cities for donor (simplified: assume they remain if at least 1 other customer)
        donor_state = cust_row['billing_state']
        donor_city = cust_row['billing_city']
        donor_remaining_cust = cust[cust['owner_id'] == donor_id]
        donor_remaining_cust = donor_remaining_cust[donor_remaining_cust['account_id'] != cust_row['account_id']]
        new_states_donor = donor_remaining_cust['billing_state'].nunique()
        new_cities_donor = donor_remaining_cust['billing_city'].nunique()
        
        # Recompute workload for donor
        term1 = new_cust_donor * 0.3
        term2 = (new_rev_donor / 1e6) / 10 * 0.4
        term3 = new_cov_donor * 0.2
        term4 = (new_states_donor * 2.0 + new_cities_donor * 0.5) * 0.1
        new_ws_donor = term1 + term2 + term3 + term4
        
        # Update for receiver
        old_cust_rec = updated_ws.loc[best_receiver, 'num_customers']
        old_rev_rec = updated_ws.loc[best_receiver, 'total_annual_revenue']
        old_contacts_rec = old_cust_rec * updated_ws.loc[best_receiver, 'coverage_rate_capped']
        new_contacts_rec = old_contacts_rec + cust_row['total_contacts']
        new_cust_rec = old_cust_rec + 1
        new_cov_rec = min(5.0, new_contacts_rec / new_cust_rec) if new_cust_rec > 0 else 0
        new_rev_rec = updated_ws.loc[best_receiver, 'total_annual_revenue'] + cust_row['annual_revenue']
        
        receiver_remaining_cust = cust[cust['owner_id'] == best_receiver]
        receiver_remaining_cust = pd.concat([receiver_remaining_cust, cust_row.to_frame().T])
        new_states_rec = receiver_remaining_cust['billing_state'].nunique()
        new_cities_rec = receiver_remaining_cust['billing_city'].nunique()
        
        term1r = new_cust_rec * 0.3
        term2r = (new_rev_rec / 1e6) / 10 * 0.4
        term3r = new_cov_rec * 0.2
        term4r = (new_states_rec * 2.0 + new_cities_rec * 0.5) * 0.1
        new_ws_rec = term1r + term2r + term3r + term4r
        
        # Check if receiver would still be within range
        if new_ws_rec > upper_bound:
            continue
        
        # Record the transfer
        transfers.append({
            'from_owner': donor_id,
            'from_name': donor_row['rep_name'],
            'to_owner': best_receiver,
            'to_name': rec_row['rep_name'],
            'account_id': cust_row['account_id'],
            'account_name': cust_row['account_name'],
            'annual_revenue': cust_row['annual_revenue'],
            'industry': cust_row['industry_normalized'],
            'state': cust_row['billing_state'],
            'donor_ws_before': donor_ws,
            'donor_ws_after': new_ws_donor,
            'receiver_ws_before': updated_ws.loc[best_receiver, 'workload_score'],
            'receiver_ws_after': new_ws_rec
        })
        
        # Update tracking
        updated_ws.loc[donor_id, 'workload_score'] = new_ws_donor
        updated_ws.loc[donor_id, 'num_customers'] = new_cust_donor
        updated_ws.loc[donor_id, 'total_annual_revenue'] = new_rev_donor
        updated_ws.loc[donor_id, 'distinct_states'] = new_states_donor
        updated_ws.loc[donor_id, 'distinct_cities'] = new_cities_donor
        updated_ws.loc[donor_id, 'coverage_rate_capped'] = new_cov_donor
        
        updated_ws.loc[best_receiver, 'workload_score'] = new_ws_rec
        updated_ws.loc[best_receiver, 'num_customers'] = new_cust_rec
        updated_ws.loc[best_receiver, 'total_annual_revenue'] = new_rev_rec
        updated_ws.loc[best_receiver, 'distinct_states'] = new_states_rec
        updated_ws.loc[best_receiver, 'distinct_cities'] = new_cities_rec
        updated_ws.loc[best_receiver, 'coverage_rate_capped'] = new_cov_rec
        
        donor_ws = new_ws_donor

print(f"\nTotal transfers proposed: {len(transfers)}")
transfers_df = pd.DataFrame(transfers)
if len(transfers) > 0:
    print("Sample transfers:")
    print(transfers_df.head(10).to_string())
    # Save to file
    transfers_df.to_csv('/work/proposed_transfers.csv', index=False)

# Check final workload distribution
final_ws = updated_ws['workload_score']
print(f"\nFinal workload stats:")
print(f"Mean: {final_ws.mean():.4f}, Std: {final_ws.std():.4f}")
print(f"Min: {final_ws.min():.4f}, Max: {final_ws.max():.4f}")
print(f"Within ±15% range: {((final_ws >= lower_bound) & (final_ws <= upper_bound)).sum()} out of {len(final_ws)}")
print(f"Below lower bound: {(final_ws < lower_bound).sum()}")
print(f"Above upper bound: {(final_ws > upper_bound).sum()}")