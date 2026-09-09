import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

res = pd.read_csv('/work/feature_clv_analysis.csv')

# Define low usage: total_visitors < 200 (47 features)
low_usage = res[res['count_visitors'] < 200].copy()
high_usage = res[res['count_visitors'] >= 200].copy()

print(f"Total features: {len(res)}")
print(f"Low usage (<200): {len(low_usage)}")
print(f"High usage (>=200): {len(high_usage)}")

# Hidden value: low usage AND positive impact AND p < 0.15 (reasonable for this analysis)
hidden = low_usage[(low_usage['ccv_diff'] > 0) & (low_usage['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print(f"\nHidden value features (low usage, positive impact, p<0.15): {len(hidden)}")
print(hidden[['feature_id','feature_name','count_visitors','product_area_name','is_core_event','avg_ccv_users','avg_ccv_nonusers','ccv_diff','p_value','n_users_tracked']].to_string())

# Also compute effect size (Cohen's d)
# Need to compute pooled std for each feature
clv_arr = np.array(res['avg_ccv_nonusers'])  # approximate

# Compute Cohen's d for each feature properly
# Using the per-visitor data
import json

# Re-load the per-visitor data
ccv_by_visitor = {}
with open('results/S29.rows.jsonl') as f:
    for line in f:
        d = json.loads(line)
        ccv_by_visitor[d['visitor_id']] = d['comprehensive_customer_value']

all_visitors = set(ccv_by_visitor.keys())

vf_data = {}
with open('results/S30.rows.jsonl') as f:
    for line in f:
        d = json.loads(line)
        vid = d['visitor_id']
        fid = d['feature_id']
        if fid not in vf_data:
            vf_data[fid] = set()
        vf_data[fid].add(vid)

cohens_d = []
for fid in res['feature_id']:
    users = vf_data.get(fid, set())
    nonusers = all_visitors - users
    u_ccv = np.array([ccv_by_visitor[v] for v in users])
    n_ccv = np.array([ccv_by_visitor[v] for v in nonusers])
    n1, n2 = len(u_ccv), len(n_ccv)
    s1, s2 = u_ccv.std(ddof=1), n_ccv.std(ddof=1)
    sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    d = (u_ccv.mean() - n_ccv.mean()) / sp if sp > 0 else 0
    cohens_d.append(d)

res['cohens_d'] = cohens_d
res.to_csv('/work/feature_clv_analysis.csv', index=False)

# Update hidden features with Cohen's d
hidden = res[(res['count_visitors'] < 200) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("\n\nHidden value features with Cohen's d:")
print(hidden[['feature_id','feature_name','count_visitors','product_area_name','ccv_diff','cohens_d','p_value']].to_string())

# Fig 1: Scatter plot of usage vs impact
plt.figure(figsize=(12, 8))
colors = ['red' if (r['count_visitors'] < 200 and r['ccv_diff'] > 0 and r['p_value'] < 0.15) else 
          'orange' if (r['count_visitors'] < 200 and r['ccv_diff'] > 0 and r['p_value'] < 0.15) else
          'blue' for _, r in res.iterrows()]

plt.scatter(res['count_visitors'], res['ccv_diff'], c=colors, alpha=0.6, s=40)
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(200, color='red', linestyle='--', alpha=0.5, label='Low usage threshold (200)')
plt.xlabel('Total Visitors (usage frequency)')
plt.ylabel('CCV Impact (avg users - avg non-users)')
plt.title('Feature Usage Frequency vs CLV Impact')
plt.legend(['Hidden Value Features', 'Other Features'])
plt.tight_layout()
plt.savefig('/work/usage_vs_impact.png', dpi=150)
print("\nSaved figure: usage_vs_impact.png")

# Fig 2: Top hidden value features - bar chart
hidden_top = hidden.head(10)
plt.figure(figsize=(14, 6))
x = range(len(hidden_top))
plt.bar(x, hidden_top['ccv_diff'].values, color='darkgreen', alpha=0.8)
plt.xticks(x, hidden_top['feature_name'].values, rotation=45, ha='right')
plt.ylabel('Average CCV Difference (users - non-users)')
plt.title('Top 10 Hidden Value Features: Low Usage, High CLV Impact')
for i, (_, r) in enumerate(hidden_top.iterrows()):
    plt.text(i, r['ccv_diff'] + 2, f"n={r['n_users_tracked']}", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/hidden_value_features.png', dpi=150)
print("Saved figure: hidden_value_features.png")