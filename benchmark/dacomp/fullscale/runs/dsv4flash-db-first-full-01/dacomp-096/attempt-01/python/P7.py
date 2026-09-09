import json, pandas as pd
import numpy as np

# Template reuse stats
cols20 = ["variation_id","campaign_type","n_uses","pct_of_type","avg_or","avg_ctor"]
rows20 = []
with open('/results/S20.rows.jsonl') as f:
    for line in f:
        rows20.append(json.loads(line))
tmpl = pd.DataFrame(rows20, columns=cols20)
print("=== Template Reuse Analysis ===")
print(tmpl.to_string(index=False))

# Overall campaign type performance
cols_an = ["flow_id","flow_name","campaign_type","audience_bucket","created_at","updated_at","prev_updated_at",
          "hours_since_prev","or_calc","mu_or","sd_or","or_anomaly","ctor_calc","mu_ctor","sd_ctor",
          "ctor_anomaly","freq_anomaly","any_anomaly"]
rows_an = []
with open('/results/S16.rows.jsonl') as f:
    for line in f:
        rows_an.append(json.loads(line))
an = pd.DataFrame(rows_an, columns=cols_an)

# Campaign type summary
print("\n\n=== Campaign Type Performance Summary ===")
type_summary = an.groupby('campaign_type').agg(
    n=('flow_id','count'),
    mean_or=('or_calc','mean'),
    std_or=('or_calc','std'),
    mean_ctor=('ctor_calc','mean'),
    std_ctor=('ctor_calc','std'),
    min_or=('or_calc','min'),
    max_or=('or_calc','max'),
    min_ctor=('ctor_calc','min'),
    max_ctor=('ctor_calc','max')
).reset_index()
type_summary = type_summary.round(4)
print(type_summary.to_string(index=False))

# Near-anomaly candidates (z-score > 1.5)
an['or_z'] = (an['or_calc'] - an['mu_or']) / an['sd_or']
an['ctor_z'] = (an['ctor_calc'] - an['mu_ctor']) / an['sd_ctor']
near_anomalies = an[(abs(an['or_z']) > 1.5) | (abs(an['ctor_z']) > 1.5)]
print("\n\n=== Near-Anomaly Campaigns (|z| > 1.5) ===")
print(near_anomalies[['flow_id','flow_name','campaign_type','or_calc','or_z','ctor_calc','ctor_z']].to_string(index=False))

# Check high-hours vs low-hours performance
print("\n\n=== Correlation: Hours Since Prev vs Performance ===")
print(an[['hours_since_prev','or_calc','ctor_calc']].corr().round(4))

# Template reuse > 50% check
print("\n\n=== Templates with >50% share within type ===")
high_reuse = tmpl[tmpl['pct_of_type'] > 50]
print(high_reuse.to_string(index=False) if len(high_reuse) > 0 else "None found")

# Overall template reuse (all campaigns)
print("\n\n=== Overall Template Usage (across all campaigns) ===")
tmpl_overall = tmpl.groupby('variation_id').agg(n_uses=('n_uses','sum'), avg_or=('avg_or','mean'), avg_ctor=('avg_ctor','mean')).reset_index()
tmpl_overall['pct_all'] = (tmpl_overall['n_uses'] / 79 * 100).round(1)
print(tmpl_overall.sort_values('n_uses', ascending=False).to_string(index=False))