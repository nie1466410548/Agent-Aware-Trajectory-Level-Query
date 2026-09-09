import json, pandas as pd, numpy as np

cust = pd.read_csv('/work/customers.csv')

# Baseline: for each rep, what % of customers are in top 3 industries?
compliance = []
for owner, grp in cust.groupby('owner_id'):
    top3 = grp['industry_normalized'].value_counts().head(3).index.tolist()
    pct = grp['industry_normalized'].isin(top3).mean()
    compliance.append({'owner_id': owner, 'n': len(grp), 'pct_top3': pct, 'n_top3': grp['industry_normalized'].isin(top3).sum(), 'top3': top3})
comp_df = pd.DataFrame(compliance)
print("Baseline compliance with 60% top-3 industry rule:")
print(comp_df['pct_top3'].describe())
print(f"Reps meeting 60%: {(comp_df['pct_top3'] >= 0.6).sum()} / {len(comp_df)}")
print(f"Reps meeting 50%: {(comp_df['pct_top3'] >= 0.5).sum()} / {len(comp_df)}")

# How many reps have all customers in different industries?
print(f"Reps with pct_top3 == 1.0: {(comp_df['pct_top3'] >= 0.999).sum()}")
print(f"Reps with pct_top3 < 0.4: {(comp_df['pct_top3'] < 0.4).sum()}")

# Check diversity: avg unique industries per rep
diversity = cust.groupby('owner_id')['industry_normalized'].nunique()
print(f"\nAvg unique industries per rep: {diversity.mean():.2f}, median: {diversity.median():.0f}")

# The workload comes mostly from revenue. Check the relationship.
# Compute the per-customer avg revenue by segment
print("\nAccount size segments:")
print(cust['account_size_segment'].value_counts())

# Distribution of customer counts per rep
print("\nCustomers per rep:")
print(cust.groupby('owner_id').size().describe())

# Examine how many customers per industry per rep (for matching)
# Check the number of state matches possible
print("\nUnique states:", cust['billing_state'].nunique())
print("Unique industries:", cust['industry_normalized'].nunique())
print("Unique cities:", cust['billing_city'].nunique())