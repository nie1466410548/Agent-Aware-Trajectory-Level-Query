import pandas as pd
import numpy as np

df = pd.read_csv('priority_scores.csv')

# Detailed breakdown of top 15
cols = ['drug_id','origin','priority_score','backlog_score','supply_interrupt_score','quality_risk_score',
        'inv_status','alert_status','total_stock','stock_to_threshold','days_since_outbound','days_since_inbound',
        'qualified','near_expiry','expired','damaged','returned','pest_mold','rodent','air_contam','temp_humidity',
        'storage_condition','transport_mode','gsp_status','disc_rate_val','zero_qualified','has_quarantine']
top15 = df.nlargest(15, 'priority_score')[cols]
pd.set_option('display.width', 250)
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', lambda x: f'{x:.1f}')
print(top15.to_string(index=False))

# Count of critical drivers among top 15
print("\n=== Driver counts among top 15 ===")
for c in ['inv_status','alert_status','zero_qualified','has_quarantine','gsp_status','storage_condition','transport_mode']:
    print(c, dict(top15[c].value_counts()))

print("\n=== Critical tier (priority >= 60) drugs ===")
crit = df[df['priority_score'] >= 60]
print(f"Count: {len(crit)}")
print(crit.groupby('origin').size())
print("\nCritical drugs detail:")
print(crit[['drug_id','origin','priority_score','backlog_score','supply_interrupt_score','quality_risk_score','inv_status','alert_status']].sort_values('priority_score', ascending=False).to_string(index=False))
