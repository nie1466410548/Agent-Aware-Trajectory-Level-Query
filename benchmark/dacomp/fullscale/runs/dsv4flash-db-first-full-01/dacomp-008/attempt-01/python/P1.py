import pandas as pd
import numpy as np
from scipy import stats

result = db.query('''
SELECT "Project Type", "Budget Amount" AS budget, "Actual Cost" AS actual,
       "Team Size" AS team, "Risk Level" AS risk, "Customer Satisfaction" AS sat,
       "Project Status" AS status, "Priority", "Completion Percentage" AS comp
FROM sheet1
''')
df = db.frame(result)
df['deviation'] = df['budget'] - df['actual']
df['dev_pct'] = (df['budget'] - df['actual']) / df['budget'] * 100
print(df.shape)
print(df.dtypes)
print(df['comp'].unique()[:10])
# clean completion percentage
df['comp_num'] = df['comp'].str.replace('%','').astype(float)
print(df[['deviation','dev_pct','team','sat']].describe())
# Save for later use
df.to_csv('/work/project_data.csv', index=False)
print("saved")
