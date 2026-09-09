import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load RFM data
with open('results/S46.rows.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
rfm = pd.DataFrame(rows, columns=['Customer ID', 'recency', 'frequency', 'monetary', 'sales', 'total_qty'])

print(rfm.shape)
print(rfm.describe())

# Recency quartiles (lower is better → higher score)
rfm['R_quartile'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1])
# Frequency quartiles (higher is better → higher score)
rfm['F_quartile'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
# Monetary quartiles (higher is better → higher score)
rfm['M_quartile'] = pd.qcut(rfm['monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])

# Convert to integers
rfm['R_score'] = rfm['R_quartile'].astype(int)
rfm['F_score'] = rfm['F_quartile'].astype(int)
rfm['M_score'] = rfm['M_quartile'].astype(int)

# Combined RFM score
rfm['RFM_total'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

# Segment labels
def segment(r, f, m):
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2 and m <= 2:
        return 'New Customers'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost'
    elif r >= 3 and f >= 4 and m >= 4:
        return 'Potential Loyalists'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Promising'
    elif r <= 2 and f >= 4 and m >= 4:
        return 'Cannot Lose Them'
    elif r <= 2 and f >= 3 and m <= 2:
        return 'Hibernating'
    elif r <= 2 and f <= 2 and m >= 3:
        return 'About to Sleep'
    else:
        return 'Others'

# Simpler approach: R+F+M score based segmentation
def segment_by_score(score):
    if score >= 10:
        return 'Top Tier'
    elif score >= 7:
        return 'Mid Tier'
    elif score >= 4:
        return 'Low Tier'
    else:
        return 'Bottom Tier'

rfm['Segment'] = rfm.apply(lambda x: segment_by_score(x['RFM_total']), axis=1)

print(rfm['Segment'].value_counts())

# Core customers (Top Tier)
top_customers = rfm[rfm['Segment'] == 'Top Tier']['Customer ID'].tolist()
print(f"Number of Top Tier customers: {len(top_customers)}")
print(f"Top Tier customers RFM stats:")
print(rfm[rfm['Segment'] == 'Top Tier'][['recency', 'frequency', 'monetary']].describe())

# Save top customers list
with open('work/top_customers.txt', 'w') as f:
    for cid in top_customers:
        f.write(cid + '\n')