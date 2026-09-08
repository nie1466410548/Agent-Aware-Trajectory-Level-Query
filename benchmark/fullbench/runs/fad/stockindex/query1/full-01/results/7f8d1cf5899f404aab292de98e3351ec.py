import json, re
import pandas as pd

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockindex/query1/full-01/results/1678feef9bfb4902a48185f0ca405ed2.json"
rows = json.load(open(path))
df = pd.DataFrame(rows)
print("rows:", len(df), df["Index"].unique())

def parse_date(s):
    s = s.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p"):
        try:
            return pd.to_datetime(s, format=fmt)
        except Exception:
            pass
    return pd.NaT

df["d"] = df["Date"].map(parse_date)
print("unparsed:", df["d"].isna().sum())
if df["d"].isna().sum():
    print(df.loc[df["d"].isna(), "Date"].unique()[:10])

df = df.dropna(subset=["d"])
df = df.drop_duplicates(subset=["Index", "d"])
since = df[df["d"] >= "2020-01-01"].copy()
print("rows since 2020 per index:")
print(since.groupby("Index").size())
print("max date:", since["d"].max(), "min:", since["d"].min())

since["vol_open"] = (since["High"] - since["Low"]) / since["Open"]
since["vol_close"] = (since["High"] - since["Low"]) / since["Close"]
since["vol_mid"] = (since["High"] - since["Low"]) / ((since["High"] + since["Low"]) / 2)

res = since.groupby("Index")[["vol_open", "vol_close", "vol_mid"]].mean().sort_values("vol_close", ascending=False)
print(res.to_string())
