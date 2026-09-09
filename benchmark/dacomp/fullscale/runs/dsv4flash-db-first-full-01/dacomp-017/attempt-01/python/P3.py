import pandas as pd
import numpy as np
import json
import os

# Load RFM data
with open('/results/S46.rows.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
rfm = pd.DataFrame(rows, columns=['Customer ID', 'recency', 'frequency', 'monetary', 'sales', 'total_qty'])

print(rfm.shape)
print(rfm.describe())

# Recency quartiles (lower recency is better → higher score)
# Use qcut - need to handle potential duplicates
rfm['R_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
# Frequency quartiles (higher is better → higher score)
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
# Monetary quartiles (higher is better → higher score)
rfm['M_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])

# Convert to integers
rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

# Combined RFM score
rfm['RFM_total'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

# Define segments
def segment_by_score(score):
    if score >= 10:
        return 'Top Tier'
    elif score >= 7:
        return 'Mid Tier'
    elif score >= 4:
        return 'Low Tier'
    else:
        return 'Bottom Tier'

rfm['Segment'] = rfm['RFM_total'].apply(segment_by_score)

print(rfm['Segment'].value_counts())

# Top customers
top_customers = rfm[rfm['Segment'] == 'Top Tier']['Customer ID'].tolist()
print(f"Number of Top Tier customers: {len(top_customers)}")
print("Top Tier RFM stats:")
print(rfm[rfm['Segment'] == 'Top Tier'][['recency', 'frequency', 'monetary']].describe())

# Save RFM results for later use
rfm.to_csv('/work/rfm_segmentation.csv', index=False)
with open('/work/top_customers.txt', 'w') as f:
    for cid in top_customers:
        f.write(cid + '\n')