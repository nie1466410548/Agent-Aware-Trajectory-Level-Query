import pandas as pd, numpy as np, json, os

# Load account features
rows = [json.loads(l) for l in open('/results/S44.rows.jsonl')]
df = pd.DataFrame(rows)
print('Shape:', df.shape)
print('Columns:', df.columns.tolist())
print('Null counts:', df.isnull().sum().to_dict())
print('Last event on range:', df['last_event_on'].min(), 'to', df['last_event_on'].max())