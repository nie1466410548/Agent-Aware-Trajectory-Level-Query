import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

res = pd.read_csv('/work/feature_clv_analysis.csv')

# Load per-visitor CLV data from archived query results
ccv_by_visitor = {}
with open('/results/S29.rows.jsonl') as f:
    for line in f:
        d = json.loads(line)
        ccv_by_visitor[d['visitor_id']] = d['comprehensive_customer_value']
all_visitors = set(ccv_by_visitor.keys())

# Load visitor-feature usage
vf_data = {}
with open('/results/S30.rows.jsonl') as f:
    for line in f:
        d = json.loads(line)
        vf_data.setdefault(d['feature_id'], set()).add(d['visitor_id'])

cohens_d = []
for fid in res['feature_id']:
    users = vf_data.get(fid, set())
    nonusers = all_visitors - users
    u_ccv = np.array([ccv_by_visitor[v] for v in users])
    n_ccv = np.array([ccv_by_visitor[v] for v in nonusers])
    n1, n2 = len(u_ccv), len(n_ccv)
    s1, s2 = u_ccv.std(ddof=1), n_ccv.std(ddof=1)
    sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    d_val = (u_ccv.mean() - n_ccv.mean()) / sp if sp > 0 else 0
    cohens_d.append(d_val)

res['cohens_d'] = cohens_d
res.to_csv('/work/feature_clv_analysis.csv', index=False)

# Hidden value: low usage (<200), positive impact, p<0.15
hidden = res[(res['count_visitors'] < 200) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("Hidden value features (low usage <200, positive impact, p<0.15):")
print(hidden[['feature_id','feature_name','count_visitors','product_area_name','is_core_event','avg_ccv_users','avg_ccv_nonusers','ccv_diff','cohens_d','p_value','n_users_tracked']].to_string())

# Summary stats
print("\nLow-usage features summary:")
print(f"  total low-usage: {len(res[res['count_visitors']<200])}")
print(f"  low-usage with positive impact: {len(res[(res['count_visitors']<200) & (res['ccv_diff']>0)])}")
print(f"  low-usage with positive impact p<0.15: {len(hidden)}")
print(f"  low-usage with negative impact: {len(res[(res['count_visitors']<200) & (res['ccv_diff']<0)])}")