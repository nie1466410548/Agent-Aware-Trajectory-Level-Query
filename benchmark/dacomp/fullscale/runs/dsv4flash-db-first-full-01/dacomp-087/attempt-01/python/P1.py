import json, os, pandas as pd, numpy as np

# Load rep scores from S19 archive
reps = []
with open('/results/S19.rows.jsonl') as f:
    for line in f:
        reps.append(json.loads(line))
rep_df = pd.DataFrame(reps)
print("rep_df shape:", rep_df.shape)
print(rep_df.head())

# Load all customers via logged interface
res = db.query("SELECT owner_id, account_id, account_name, annual_revenue, billing_state, billing_city, industry_normalized, account_size_segment, total_contacts, number_of_employees, total_opportunities, won_opportunities, win_rate_percentage FROM salesforce__customer_360_view")
cust = db.frame(res)
print("cust shape:", cust.shape)
print(cust.head())
cust.to_csv('/work/customers.csv', index=False)
rep_df.to_csv('/work/reps.csv', index=False)