import json, pandas as pd

def load(sid, cols):
    rows=[]
    with open(f'/results/S{sid}.rows.jsonl') as f:
        for line in f: rows.append(json.loads(line))
    df = pd.DataFrame(rows, columns=cols)
    return df

sleep_df = load(14, ['Sleep duration','total','yes_n','yes_pct'])
print("S14 rows:")
for r in sleep_df.itertuples(index=False): print([repr(x) for x in r])

acad_df = load(16, ['acad_group','total','yes_n','yes_pct'])
print("S16 rows:")
for r in acad_df.itertuples(index=False): print([repr(x) for x in r])
