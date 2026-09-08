import json, pandas as pd

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query10/full-01/results/"
cases = pd.read_json(base + "a477db37dccb48c4bc6e1249a4f1c8bb.json")
hist = pd.read_json(base + "a791c08b30a4452c894506874b295a12.json")

# clean stray '#' prefixes seen in some id fields
cases["id"] = cases["id"].str.lstrip("#")
cases["ownerid"] = cases["ownerid"].str.lstrip("#")
hist["caseid__c"] = hist["caseid__c"].str.lstrip("#")
hist["newvalue__c"] = hist["newvalue__c"].str.lstrip("#")
hist["oldvalue__c"] = hist["oldvalue__c"].str.lstrip("#")

for c in ["createddate", "closeddate"]:
    cases[c] = pd.to_datetime(cases[c], utc=True, errors="coerce")
hist["createddate"] = pd.to_datetime(hist["createddate"], utc=True, errors="coerce")

today = pd.Timestamp("2023-09-02", tz="UTC")
start = today - pd.DateOffset(months=4)
print("window:", start, "to", today)

# transferred = more than one Owner Assignment row
oa_counts = hist.groupby("caseid__c").size()
transferred = set(oa_counts[oa_counts > 1].index)
print("transferred cases:", len(transferred))

# agent involvement (first-assigned OR transferred-to): any newvalue assignment
involve = hist[["newvalue__c", "caseid__c"]].dropna().rename(
    columns={"newvalue__c": "agent", "caseid__c": "caseid"}).drop_duplicates()

cases["ht_hours"] = (cases["closeddate"] - cases["createddate"]).dt.total_seconds() / 3600

def run(window_col, count_scope):
    # handle-time rows: closed, not transferred, case in window by window_col
    in_win = cases[(cases[window_col] >= start) & (cases[window_col] <= today)]
    ht = in_win[in_win["closeddate"].notna() & ~in_win["id"].isin(transferred)]
    avg = ht.groupby("ownerid")["ht_hours"].agg(["mean", "count"])
    # processed count
    if count_scope == "window":
        win_ids = set(in_win["id"])
        inv = involve[involve["caseid"].isin(win_ids)]
    else:
        inv = involve
    cnt = inv.groupby("agent")["caseid"].nunique()
    df = avg.join(cnt.rename("processed"), how="inner")
    df = df[df["processed"] > 1].sort_values("mean")
    return df

for wc in ["closeddate", "createddate"]:
    for cs in ["window", "alltime"]:
        print(f"\n=== window_col={wc}, count_scope={cs} ===")
        print(run(wc, cs))
