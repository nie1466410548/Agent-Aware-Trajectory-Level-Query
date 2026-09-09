import pandas as pd
import numpy as np

postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
active = postings[postings['state'].isin(['published', 'pending'])]

# Opportunity metrics per department
opp_metrics = active.groupby('categories_department').agg(
    active_postings=('posting_id', 'count'),
    total_opportunities=('count_opportunities', 'sum'),
    open_opportunities=('count_open_opportunities', 'sum'),
    interviews=('count_interviews', 'sum'),
    applications=('count_posting_applications', 'sum'),
    distinct_hms=('posting_hiring_manager_name', 'nunique')
).reset_index()
opp_metrics['open_opp_per_posting'] = opp_metrics['open_opportunities'] / opp_metrics['active_postings']
opp_metrics['open_opp_per_hm'] = opp_metrics['open_opportunities'] / opp_metrics['distinct_hms']
print("Active posting opportunity metrics per department:")
print(opp_metrics.to_string(index=False))

# Also all postings
all_metrics = postings.groupby('categories_department').agg(
    all_postings=('posting_id', 'count'),
    total_opportunities=('count_opportunities', 'sum'),
    open_opportunities=('count_open_opportunities', 'sum'),
    interviews=('count_interviews', 'sum'),
    distinct_hms=('posting_hiring_manager_name', 'nunique')
).reset_index()
all_metrics['open_opp_per_posting'] = all_metrics['open_opportunities'] / all_metrics['all_postings']
all_metrics['open_opp_per_hm'] = all_metrics['open_opportunities'] / all_metrics['distinct_hms']
print("\nAll posting opportunity metrics per department:")
print(all_metrics.to_string(index=False))

# Check pending state postings per department
pending = postings[postings['state'] == 'pending']
print("\nPending state postings per department:")
print(pending.groupby('categories_department').agg(
    pending_cnt=('posting_id', 'count'),
    distinct_hms=('posting_hiring_manager_name', 'nunique')
))

# pending + published
print("\nPublished + Pending postings per dept, with distinct HMs:")
print(active.groupby('categories_department').agg(
    cnt=('posting_id', 'count'),
    hms=('posting_hiring_manager_name', 'nunique')
))