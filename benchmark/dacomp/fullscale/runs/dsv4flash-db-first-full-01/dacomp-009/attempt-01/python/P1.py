import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load the full ranked table from the archived result of query S27
with open('/results/S27.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
df = pd.DataFrame(rows)
df.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
              'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']
print(df.shape)
print(df.head())
print(df['Gender'].value_counts())
print(df['Education Level'].value_counts())
print(df['Team'].value_counts())
print("Rank range male:", df.loc[df.Gender=='Male','rank'].min(), df.loc[df.Gender=='Male','rank'].max())
