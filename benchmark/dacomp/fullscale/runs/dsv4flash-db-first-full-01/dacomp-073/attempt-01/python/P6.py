import pandas as pd
import numpy as np
from collections import Counter

postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
requisitions = db.frame(db.query("SELECT * FROM lever__requisition_enhanced"))

# Map hiring manager name -> most common department
hm_dept = {}
for name, grp in postings.groupby('posting_hiring_manager_name'):
    hm_dept[name] = grp['categories_department'].mode()[0]

# Map requisitions to department via owner_name and creator_name
requisitions['dept_by_owner'] = requisitions['owner_name'].map(hm_dept)
requisitions['dept_by_creator'] = requisitions['creator_name'].map(hm_dept)
requisitions['dept_name_map'] = requisitions['dept_by_owner'].fillna(requisitions['dept_by_creator'])

open_reqs = requisitions[requisitions['status'] == 'open']
print("Open requisitions mapped via owner/creator name:")
print(open_reqs['dept_name_map'].value_counts(dropna=False))

# Combine all mapping strategies for open reqs
requisitions['dept'] = requisitions['dept_name_map']
# For unmapped, try hiring manager user ID mapping
user_dept = {}
for uid in requisitions['hiring_manager_user_id'].dropna().unique():
    depts = []
    for _, row in postings[postings['owner_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    for _, row in postings[postings['creator_user_id'] == uid].iterrows():
        depts.append(row['categories_department'])
    if depts:
        user_dept[uid] = Counter(depts).most_common(1)[0][0]

requisitions['dept'] = requisitions['dept'].fillna(requisitions['hiring_manager_user_id'].map(user_dept))
requisitions['dept'] = requisitions['dept'].fillna('Unmapped')

print("\nOpen requisitions per dept (combined mapping):")
print(requisitions[requisitions['status']=='open']['dept'].value_counts(dropna=False))

# Also look at pending (open+on-hold)
print("\nPending (open+on-hold) reqs per dept (combined mapping):")
print(requisitions[requisitions['status'].isin(['open','on-hold'])]['dept'].value_counts(dropna=False))

# Headcount-based pending roles: count reqs still needing headcount
def pending_roles(row):
    if row['status'] != 'open':
        return 0
    if row['headcount_infinite'] == 1:
        return 1  # infinite means always hiring at least 1
    if row['headcount_total'] > row['headcount_hired']:
        return row['headcount_total'] - row['headcount_hired']
    return 0

requisitions['pending_roles_count'] = requisitions.apply(pending_roles, axis=1)
print("\nHeadcount-based pending roles per dept (open reqs):")
print(requisitions.groupby('dept')['pending_roles_count'].sum().sort_values(ascending=False))

# Total open reqs count per dept
print("\nOpen req COUNT per dept:")
print(requisitions[requisitions['status']=='open'].groupby('dept').size().sort_values(ascending=False))