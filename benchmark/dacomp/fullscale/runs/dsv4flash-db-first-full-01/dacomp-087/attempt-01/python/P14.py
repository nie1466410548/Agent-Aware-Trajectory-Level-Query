import pandas as pd, numpy as np

cust = pd.read_csv('/work/customers.csv')
cust['account_id'] = cust['account_id'].astype(str)
transfers_df = pd.read_csv('/work/final_transfers.csv')
transfers_df['account_id'] = transfers_df['account_id'].astype(str)

# Top 10 transfers by revenue
print("===== TOP 10 TRANSFERS BY REVENUE =====")
cols = ['from_name', 'to_name', 'revenue', 'industry', 'state', 'segment', 'donor_ws_before', 'donor_ws_after', 'rec_ws_before', 'rec_ws_after']
print(transfers_df.sort_values('revenue', ascending=False)[cols].head(10).to_string())

# Summary by donor
print("\n===== TOP DONORS (by total revenue moved out) =====")
donor_summary = transfers_df.groupby(['from_owner', 'from_name']).agg(
    n_moved=('account_id', 'count'),
    revenue_moved=('revenue', 'sum'),
    avg_donor_ws_drop=('donor_ws_before', lambda x: (transfers_df.loc[x.index, 'donor_ws_before'] - transfers_df.loc[x.index, 'donor_ws_after']).mean())
).sort_values('revenue_moved', ascending=False).head(8)
print(donor_summary.to_string())

# Summary by receiver
print("\n===== TOP RECEIVERS (by total revenue received) =====")
rec_summary = transfers_df.groupby(['to_owner', 'to_name']).agg(
    n_received=('account_id', 'count'),
    revenue_received=('revenue', 'sum'),
    avg_rec_ws_gain=('rec_ws_after', lambda x: (transfers_df.loc[x.index, 'rec_ws_after'] - transfers_df.loc[x.index, 'rec_ws_before']).mean())
).sort_values('revenue_received', ascending=False).head(8)
print(rec_summary.to_string())

# Workload range summary
fw = pd.read_csv('/work/final_workloads.csv', index_col=0)
print("\n===== FINAL WORKLOAD (select reps) =====")
print("All reps within [5.04, 10.05]; mean={:.2f}, std={:.2f}".format(fw['workload'].mean(), fw['workload'].std()))

# Check how many reps still outside range
avg_ws = 8.741
lo, hi = avg_ws*0.85, avg_ws*1.15
below = (fw['workload'] < lo).sum()
above = (fw['workload'] > hi).sum()
print(f"Below {lo:.2f}: {below}, Above {hi:.2f}: {above}")

# Save transfer plan excerpt
transfers_df[cols].head(50).to_csv('/work/top_transfers_excerpt.csv', index=False)