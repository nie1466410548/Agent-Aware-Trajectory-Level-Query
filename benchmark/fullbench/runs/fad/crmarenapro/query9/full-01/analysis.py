import json, pandas as pd

cases = pd.DataFrame(json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query9/full-01/results/81db1b57860d48079805d0f26e074724.json")))
accts = pd.DataFrame(json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query9/full-01/results/27817dfc54fa4029b3781ba1291f01a8.json")))

cases["accountid"] = cases["accountid"].str.lstrip("#")
accts["Id"] = accts["Id"].str.lstrip("#")

df = cases.merge(accts, left_on="accountid", right_on="Id", how="left")
df["created"] = pd.to_datetime(df["createddate"], utc=True)
df["closed"] = pd.to_datetime(df["closeddate"], utc=True)
df["hours"] = (df["closed"] - df["created"]).dt.total_seconds() / 3600.0

print("Unmatched accounts:", df["ShippingState"].isna().sum())
res = df.groupby("ShippingState")["hours"].agg(["mean","median","count"]).sort_values("mean")
print(res)
print("\nFastest by mean:", res.index[0])
