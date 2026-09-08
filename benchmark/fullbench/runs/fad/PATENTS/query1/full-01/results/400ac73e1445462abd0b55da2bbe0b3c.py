import json
import pandas as pd

COUNTS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query1/full-01/results/a35028c05c3d48d990e8729ea7decdb3.json"
counts = pd.DataFrame(json.load(open(COUNTS)))
dropped = ['A16B', 'A23Y', 'C12B', 'F24J', 'G21Y', 'Z03R']
d = counts[counts["subclass"].isin(dropped)]
print(d.groupby("subclass")["n"].sum())
ymin, ymax = int(counts["yr"].min()), int(counts["yr"].max())
for sc in dropped:
    s = counts[counts["subclass"] == sc].set_index("yr")["n"].reindex(range(ymin, ymax + 1), fill_value=0)
    ema = s.ewm(alpha=0.2, adjust=False).mean()
    print(sc, "EMA2022 =", round(ema[2022], 3))
