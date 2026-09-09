import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 150

s1 = db.frame(db.query("SELECT * FROM sheet1 ORDER BY \"Promotion Date\""))
s2 = db.frame(db.query("SELECT * FROM sheet2 ORDER BY \"Promotion Date\""))
s1['dt'] = pd.to_datetime(s1['Promotion Date'])
s2['dt'] = pd.to_datetime(s2['Promotion Date'])

# Daily market totals from sheet2 (all 73 categories)
daily2 = s2.groupby('dt').agg(
    orders=('T+0 strategy-guided order count', 'sum'),
    tx_amt=('T+0 strategy-guided transaction amount', 'sum'),
    n_cat=('Promotion Tertiary Category', 'nunique')
).reset_index()
daily2['dow'] = daily2['dt'].dt.day_name()
print("=== Sheet2 daily totals (ALL categories, market context) ===")
print(daily2.to_string(index=False))

# Daily totals from sheet1 (all strategy rows)
s1['spend'] = s1['Spend (Yuan)']
s1['clicks'] = s1['Clicks']
s1['impressions'] = s1['Impressions']
daily1 = s1.groupby('dt').agg(
    spend=('spend', 'sum'),
    impressions=('impressions', 'sum'),
    clicks=('clicks', 'sum'),
    n_rows=('Strategy', 'count')
).reset_index()
daily1['dow'] = daily1['dt'].dt.day_name()
print("\n=== Sheet1 daily totals (strategy campaign rows) ===")
print(daily1.to_string(index=False))

# Check duplicates in sheet2 on (dt, category)
dup = s2.groupby(['dt', 'Promotion Tertiary Category']).size()
print("\nDuplicate (dt, category) keys in sheet2:", (dup > 1).sum())
print(dup[dup > 1])
