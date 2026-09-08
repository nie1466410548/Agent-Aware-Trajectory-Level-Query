import json
import pandas as pd

res_dir = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query4/full-01/results/"

with open(res_dir + "54cb27131cf94d8f83d7ad76c9d81229.json") as f:
    counts = json.load(f)
with open(res_dir + "6e9e4ba4a4aa4132824e267e2d1a0f75.json") as f:
    info = {r["Symbol"]: r["Company Description"] for r in json.load(f)}

df = pd.DataFrame(counts)
qual = df[df["up_days"] > df["down_days"]].copy()
print("qualifying stocks:", len(qual))

qual = qual.sort_values(["up_days", "Symbol"], ascending=[False, True])
print(qual.head(15).to_string())

top5 = qual.head(5)
for _, r in top5.iterrows():
    print("\n---", r["Symbol"], "up:", r["up_days"], "down:", r["down_days"])
    print(info[r["Symbol"]])
