import json, pandas as pd
import numpy as np

cols_an = ["flow_id","flow_name","campaign_type","audience_bucket","created_at","updated_at","prev_updated_at",
          "hours_since_prev","or_calc","mu_or","sd_or","or_anomaly","ctor_calc","mu_ctor","sd_ctor",
          "ctor_anomaly","freq_anomaly","any_anomaly"]
rows_an = []
with open('/results/S16.rows.jsonl') as f:
    for line in f:
        rows_an.append(json.loads(line))
an = pd.DataFrame(rows_an, columns=cols_an)
an['created_at'] = pd.to_datetime(an['created_at'])
an['hour_sent'] = an['created_at'].dt.hour
an['is_weekend'] = an['created_at'].dt.dayofweek.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
an['daypart'] = an['hour_sent'].apply(lambda x: 'Morning' if x < 12 else 'Afternoon')
an['or_z'] = (an['or_calc'] - an['mu_or']) / an['sd_or']
an['ctor_z'] = (an['ctor_calc'] - an['mu_ctor']) / an['sd_ctor']
an['variant_letter'] = an['flow_name'].str.extract(r'Variant ([A-C])')

# Near-anomaly root cause analysis
near = an[(abs(an['or_z']) > 1.5) | (abs(an['ctor_z']) > 1.5)]
print("=== Near-Anomaly Campaign Root Cause Analysis ===")
print(near[['flow_id','flow_name','campaign_type','created_at','is_weekend','daypart','variant_letter',
            'or_calc','or_z','ctor_calc','ctor_z']].to_string(index=False))

# Template reuse for near-anomaly campaigns
print("\n\n=== Template (variation_id) for near-anomaly campaigns ===")
cols20 = ["variation_id","campaign_type","n_uses","pct_of_type","avg_or","avg_ctor"]
rows20 = []
with open('/results/S20.rows.jsonl') as f:
    for line in f:
        rows20.append(json.loads(line))
tmpl = pd.DataFrame(rows20, columns=cols20)

# FLOW-1004: Cart Recovery Series - Variant A → VAR-004
# FLOW-1006: Cart Recovery Series - Variant C → VAR-006
# FLOW-1013: Winback Journey - Variant A → VAR-013
# FLOW-1021: Seasonal Warmup Flow - Variant C → VAR-021
# FLOW-1036: Post-Purchase Journey - Variant C → VAR-012
# FLOW-1070: Product Discovery Flow - Variant A → VAR-022

near_templates = {
    'FLOW-1004': 'VAR-004', 'FLOW-1006': 'VAR-006', 'FLOW-1013': 'VAR-013',
    'FLOW-1021': 'VAR-021', 'FLOW-1036': 'VAR-012', 'FLOW-1070': 'VAR-022'
}
for fid, vid in near_templates.items():
    t = tmpl[tmpl['variation_id'] == vid]
    if len(t) > 0:
        print(f"{fid} ({vid}): {t.iloc[0]['campaign_type']}, n_uses={t.iloc[0]['n_uses']}, "
              f"pct_in_type={t.iloc[0]['pct_of_type']}%, avg_or={t.iloc[0]['avg_or']:.4f}, avg_ctor={t.iloc[0]['avg_ctor']:.4f}")

# Average performance by variant letter across all campaign types
print("\n\n=== Performance by Variant (Copy Theme Proxy) ===")
v_agg = an.groupby('variant_letter').agg(
    n=('flow_id','count'), mean_or=('or_calc','mean'), mean_ctor=('ctor_calc','mean')
).reset_index()
print(v_agg.round(4).to_string(index=False))

# Per campaign type - best variant
print("\n\n=== Best Performing Variant per Campaign Type ===")
best_v = an.groupby(['campaign_type','variant_letter']).agg(
    mean_or=('or_calc','mean'), mean_ctor=('ctor_calc','mean'), n=('flow_id','count')
).reset_index()
best_v = best_v.sort_values(['campaign_type','mean_ctor'], ascending=[True,False])
for ct in best_v['campaign_type'].unique():
    sub = best_v[best_v['campaign_type']==ct].head(1)
    r = sub.iloc[0]
    print(f"{ct}: Best Variant {r['variant_letter']} (OR={r['mean_or']:.4f}, CTOR={r['mean_ctor']:.4f})")

# Gaps between best and worst variant per type
print("\n\n=== Performance Gap: Variant C vs Variant A ===")
for ct in an['campaign_type'].unique():
    sub = an[an['campaign_type']==ct]
    c = sub[sub['variant_letter']=='C']
    a = sub[sub['variant_letter']=='A']
    if len(c) > 0 and len(a) > 0:
        or_gap = c['or_calc'].mean() - a['or_calc'].mean()
        ctor_gap = c['ctor_calc'].mean() - a['ctor_calc'].mean()
        print(f"{ct}: OR +{or_gap:.4f} ({or_gap/a['or_calc'].mean()*100:.1f}%), CTOR +{ctor_gap:.4f} ({ctor_gap/a['ctor_calc'].mean()*100:.1f}%)")