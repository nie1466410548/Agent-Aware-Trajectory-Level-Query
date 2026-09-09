import pandas as pd
import numpy as np
from collections import Counter

postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
requisitions = db.frame(db.query("SELECT * FROM lever__requisition_enhanced"))

# Requisition monthly counts
requisitions['ym'] = requisitions['created_at'].str[:7]
print("Requisition monthly counts:")
print(requisitions.groupby('ym').size())

# Open requisitions monthly
open_req = requisitions[requisitions['status'] == 'open']
print("\nOpen requisitions monthly:")
print(open_req.groupby('ym').size())

# Map requisitions to departments via all available methods
# Method 1: owner_name -> posting_hiring_manager_name -> dept
hm_dept = {}
for name, grp in postings.groupby('posting_hiring_manager_name'):
    hm_dept[name] = grp['categories_department'].mode()[0]

# Method 2: hiring_manager_user_id -> posting owner/creator -> dept
user_dept = {}
for uid in requisitions['hiring_manager_user_id'].dropna().unique():
    depts = []
    for _, row in postings[postings['owner_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    for _, row in postings[postings['creator_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    if depts:
        user_dept[uid] = Counter(depts).most_common(1)[0][0]

# Combined mapping
requisitions['dept'] = None
mask = requisitions['owner_name'].isin(hm_dept)
requisitions.loc[mask, 'dept'] = requisitions.loc[mask, 'owner_name'].map(hm_dept)
mask = requisitions['dept'].isna() & requisitions['creator_name'].isin(hm_dept)
requisitions.loc[mask, 'dept'] = requisitions.loc[mask, 'creator_name'].map(hm_dept)
mask = requisitions['dept'].isna() & requisitions['hiring_manager_user_id'].isin(user_dept)
requisitions.loc[mask, 'dept'] = requisitions.loc[mask, 'hiring_manager_user_id'].map(user_dept)
requisitions['dept'] = requisitions['dept'].fillna('Unmapped')

# Open reqs per dept per month
open_req = requisitions[requisitions['status'] == 'open']
print("\nOpen reqs per dept:")
print(open_req.groupby('dept').size().sort_values(ascending=False))

# Active HMs per dept from postings
active = postings[postings['state'].isin(['published', 'pending'])]
active_hms = active.groupby('categories_department')['posting_hiring_manager_name'].nunique()
all_hms = postings.groupby('categories_department')['posting_hiring_manager_name'].nunique()

print("\nActive HMs per dept:")
print(active_hms)
print("\nAll HMs per dept:")
print(all_hms)

# Compute pressure index = open reqs / active HMs for mapped depts
departments = ['Engineering', 'Finance', 'HR', 'Marketing', 'Operations', 'Sales']
print("\n=== Pressure Index with open reqs / active HMs ===")
for dept in departments:
    open_cnt = len(open_req[open_req['dept'] == dept])
    hm = active_hms.get(dept, 1)
    pi = open_cnt / hm
    print(f"{dept}: open_reqs={open_cnt}, active_HMs={hm}, PI={pi:.4f}")

# Compute pressure index = open reqs / all HMs
print("\n=== Pressure Index with open reqs / all HMs ===")
for dept in departments:
    open_cnt = len(open_req[open_req['dept'] == dept])
    hm = all_hms.get(dept, 1)
    pi = open_cnt / hm
    print(f"{dept}: open_reqs={open_cnt}, all_HMs={hm}, PI={pi:.4f}")

# Compute pressure index with pending (open+on-hold) reqs
pending_req = requisitions[requisitions['status'].isin(['open', 'on-hold'])]
print("\n=== Pressure Index with pending (open+on-hold) reqs / active HMs ===")
for dept in departments:
    pending_cnt = len(pending_req[pending_req['dept'] == dept])
    hm = active_hms.get(dept, 1)
    pi = pending_cnt / hm
    print(f"{dept}: pending_reqs={pending_cnt}, active_HMs={hm}, PI={pi:.4f}")

# Compute pressure index with sum of count_postings from open reqs
print("\n=== Pressure Index with count_postings from open reqs / active HMs ===")
open_req_postings = open_req.groupby('dept')['count_postings'].sum()
for dept in departments:
    postings_cnt = open_req_postings.get(dept, 0)
    hm = active_hms.get(dept, 1)
    pi = postings_cnt / hm
    print(f"{dept}: count_postings={postings_cnt:.0f}, active_HMs={hm}, PI={pi:.4f}")

# What about total postings per dept including all states?
print("\n=== Pressure Index with total postings / all HMs ===")
total_postings = postings.groupby('categories_department').size()
for dept in departments:
    pi = total_postings.get(dept, 0) / all_hms.get(dept, 1)
    print(f"{dept}: total={total_postings.get(dept,0)}, all_HMs={all_hms.get(dept,1)}, PI={pi:.4f}")