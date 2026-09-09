import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

res = pd.read_csv('/work/feature_clv_analysis.csv')

# Load per-visitor CLV data (rows are arrays: [visitor_id, ccv, uvs])
ccv_by_visitor = {}
with open('/results/S29.rows.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        arr = json.loads(line)
        ccv_by_visitor[arr[0]] = arr[1]
all_visitors = set(ccv_by_visitor.keys())
print("Tracked visitors:", len(all_visitors))

# Load visitor-feature usage (rows: [visitor_id, feature_id, sum_clicks, active_days, click_events, minutes])
vf_data = {}
with open('/results/S30.rows.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        arr = json.loads(line)
        vf_data.setdefault(arr[1], set()).add(arr[0])
print("Features in vf:", len(vf_data))

cohens_d = []
for fid in res['feature_id']:
    users = vf_data.get(fid, set())
    nonusers = all_visitors - users
    u_ccv = np.array([ccv_by_visitor[v] for v in users])
    n_ccv = np.array([ccv_by_visitor[v] for v in nonusers])
    n1, n2 = len(u_ccv), len(n_ccv)
    if n1 > 1 and n2 > 1:
        s1, s2 = u_ccv.std(ddof=1), n_ccv.std(ddof=1)
        sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
        d_val = (u_ccv.mean() - n_ccv.mean()) / sp if sp > 0 else 0
    else:
        d_val = 0
    cohens_d.append(d_val)

res['cohens_d'] = cohens_d
res.to_csv('/work/feature_clv_analysis.csv', index=False)

# Hidden value features
hidden = res[(res['count_visitors'] < 200) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("\nHidden value features (low usage <200, positive impact, p<0.15):")
print(hidden[['feature_id','feature_name','count_visitors','product_area_name','is_core_event','avg_ccv_users','avg_ccv_nonusers','ccv_diff','cohens_d','p_value','n_users_tracked']].to_string())

print("\nLow-usage summary:")
print("  low-usage total:", len(res[res['count_visitors']<200]))
print("  low-usage positive impact:", len(res[(res['count_visitors']<200) & (res['ccv_diff']>0)]))
print("  low-usage positive & p<0.15:", len(hidden))
print("  low-usage negative impact:", len(res[(res['count_visitors']<200) & (res['ccv_diff']<0)]))

# Top features overall by impact
print("\nTop 10 features by positive impact (all):")
print(res.sort_values('ccv_diff', ascending=False).head(10)[['feature_name','count_visitors','ccv_diff','cohens_d','p_value']].to_string())