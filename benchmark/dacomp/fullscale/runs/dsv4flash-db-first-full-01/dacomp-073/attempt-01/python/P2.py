import pandas as pd
import numpy as np

# Get all postings data
postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
requisitions = db.frame(db.query("SELECT * FROM lever__requisition_enhanced"))

print("Postings columns:", postings.columns.tolist())
print("Requisitions columns:", requisitions.columns.tolist())
print(f"\nPostings shape: {postings.shape}")
print(f"Requisitions shape: {requisitions.shape}")

# Check date ranges
print(f"\nPostings created_at range: {postings['created_at'].min()} to {postings['created_at'].max()}")
print(f"Postings updated_at range: {postings['updated_at'].min()} to {postings['updated_at'].max()}")
print(f"Requisitions created_at range: {requisitions['created_at'].min()} to {requisitions['created_at'].max()}")

# Check department distribution
print("\nDepartments:")
print(postings['categories_department'].value_counts())

# State distribution
print("\nState distribution:")
print(postings['state'].value_counts())

# Requisition status
print("\nRequisition status:")
print(requisitions['status'].value_counts())

# Monthly postings
postings['ym'] = postings['created_at'].str[:7]
print("\nMonthly postings:")
print(postings.groupby('ym').size())

# Monthly per department
print("\nMonthly postings per department:")
print(postings.groupby(['categories_department', 'ym']).size().unstack(fill_value=0))

# Active postings per department
active = postings[postings['state'].isin(['published', 'pending'])]
print("\nActive postings per department:")
print(active['categories_department'].value_counts())

# Hiring managers per department
print("\nDistinct hiring managers per department:")
print(postings.groupby('categories_department')['posting_hiring_manager_name'].nunique())

# Active hiring managers per department
print("\nActive hiring managers per department:")
print(active.groupby('categories_department')['posting_hiring_manager_name'].nunique())

# Check if owner_name/creator_name in requisitions matches posting_hiring_manager_name
print("\nOverlap between req owner_name and posting_hiring_manager_name:")
print(requisitions['owner_name'].isin(postings['posting_hiring_manager_name'].unique()).sum())

print("Overlap between req creator_name and posting_hiring_manager_name:")
print(requisitions['creator_name'].isin(postings['posting_hiring_manager_name'].unique()).sum())

# Check the mapping between requisition hiring_manager_user_id and posting user IDs
req_hm_ids = set(requisitions['hiring_manager_user_id'].unique())
post_owner_ids = set(postings['owner_user_id'].dropna().unique())
post_creator_ids = set(postings['creator_user_id'].dropna().unique())
print(f"\nRequisition hiring manager user IDs: {len(req_hm_ids)}")
print(f"Posting owner user IDs: {len(post_owner_ids)}")
print(f"Posting creator user IDs: {len(post_creator_ids)}")
print(f"Overlap with owner: {len(req_hm_ids & post_owner_ids)}")
print(f"Overlap with creator: {len(req_hm_ids & post_creator_ids)}")

# Create a mapping from user ID to department
# For each user, find the most common department
user_dept_map = {}
for uid in req_hm_ids:
    depts = []
    for _, row in postings[postings['owner_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    for _, row in postings[postings['creator_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    if depts:
        from collections import Counter
        user_dept_map[uid] = Counter(depts).most_common(1)[0][0]

print(f"\nMapped HMs to departments: {len(user_dept_map)}")

# Map requisitions to departments
requisitions['department'] = requisitions['hiring_manager_user_id'].map(user_dept_map)
requisitions['department'] = requisitions['department'].fillna('Unmapped')

# Open requisitions per department
open_reqs = requisitions[requisitions['status'] == 'open']
print("\nOpen requisitions per department:")
print(open_reqs['department'].value_counts())

# Pending roles (open + on-hold) per department
pending_reqs = requisitions[requisitions['status'].isin(['open', 'on-hold'])]
print("\nPending (open + on-hold) requisitions per department:")
print(pending_reqs['department'].value_counts())

# Total requisitions per department
print("\nAll requisitions per department:")
print(requisitions['department'].value_counts())