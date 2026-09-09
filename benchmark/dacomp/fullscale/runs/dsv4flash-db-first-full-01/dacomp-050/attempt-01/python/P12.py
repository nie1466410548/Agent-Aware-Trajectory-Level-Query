import json, pandas as pd

def load(sid, cols):
    rows=[]
    with open(f'/results/S{sid}.rows.jsonl') as f:
        for line in f: rows.append(json.loads(line))
    return pd.DataFrame(rows, columns=cols)

ds_df = load(25, ['Dietary habits','sleep_cat','total','yes_n','yes_pct'])
print(ds_df)
print(ds_df.dtypes)
print("unique diet:", ds_df['Dietary habits'].unique())
print("unique sleep:", ds_df['sleep_cat'].unique())

risk_df = load(29, ['n_risk','total','yes_n','yes_pct'])
print(risk_df)
