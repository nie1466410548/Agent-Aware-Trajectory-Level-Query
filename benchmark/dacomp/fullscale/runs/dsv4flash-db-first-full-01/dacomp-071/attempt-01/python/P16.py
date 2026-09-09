import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Deep dive into the bottleneck stages
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, job_title, application_sources
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment', 'Final Interview')
"""))

# For Technical Assessment, look at terminal (attrition) vs non-terminal
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

# Terminal = attrited at this stage
df['terminal'] = ~df['has_next']

# For Technical Assessment
ta = df[df['stage'] == 'Technical Assessment']
ta_attrited = ta[ta['terminal']]
ta_advanced = ta[~ta['terminal']]

print("=== TECHNICAL ASSESSMENT ===")
print(f"Total: {len(ta)}, Attrited: {len(ta_attrited)}, Advanced: {len(ta_advanced)}")
print("\nAttrition reasons at Technical Assessment (terminal entries):")
print(ta_attrited['archive_reason'].value_counts().to_string())
print(f"\nAvg days - Attrited: {ta_attrited['days_in_stage'].mean():.1f}, Advanced: {ta_advanced['days_in_stage'].mean():.1f}")
print("\nBy job_team (attrited):")
print(ta_attrited.groupby('job_team').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).to_string())
print("\nBy application_sources (attrited):")
print(ta_attrited.groupby('application_sources').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).to_string())

# For Final Interview
fi = df[df['stage'] == 'Final Interview']
fi_attrited = fi[fi['terminal']]
fi_advanced = fi[~fi['terminal']]

print("\n=== FINAL INTERVIEW ===")
print(f"Total: {len(fi)}, Attrited: {len(fi_attrited)}, Advanced: {len(fi_advanced)}")
print("\nAttrition reasons at Final Interview:")
print(fi_attrited['archive_reason'].value_counts().to_string())
print(f"\nAvg days - Attrited: {fi_attrited['days_in_stage'].mean():.1f}, Advanced: {fi_advanced['days_in_stage'].mean():.1f}")
print("\nBy job_team (attrited):")
print(fi_attrited.groupby('job_team').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).to_string())
print("\nBy application_sources (attrited):")
print(fi_attrited.groupby('application_sources').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).to_string())

# Also check if there are any patterns in days_in_stage distribution
print("\n=== DAYS DISTRIBUTION ===")
for stage_name in ['Technical Assessment', 'Final Interview']:
    s = df[df['stage'] == stage_name]
    print(f"\n{stage_name}:")
    print(f"  Percentiles: 25th={s['days_in_stage'].quantile(0.25):.0f}, 50th={s['days_in_stage'].median():.0f}, 75th={s['days_in_stage'].quantile(0.75):.0f}")
    print(f"  90th={s['days_in_stage'].quantile(0.9):.0f}, 95th={s['days_in_stage'].quantile(0.95):.0f}")