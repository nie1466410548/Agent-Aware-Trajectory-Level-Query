import json
import pandas as pd

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/stockindex/query2/quick-01/results/a57fa6e821f544e8af61d0f36395a1b1.json"
with open(path) as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
# Parse mixed date formats
df["dt"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True)
# sanity: all in 2018
print("All rows year 2018:", (df["dt"].dt.year == 2018).all())
print("Rows per index:", df.groupby("Index").size().to_dict())

df["up"] = df["Close"] > df["Open"]
df["down"] = df["Close"] < df["Open"]
df["flat"] = df["Close"] == df["Open"]

summary = df.groupby("Index").agg(
    total=("Close", "size"),
    up_days=("up", "sum"),
    down_days=("down", "sum"),
    flat_days=("flat", "sum"),
)
summary["more_up_than_down"] = summary["up_days"] > summary["down_days"]
print(summary)
