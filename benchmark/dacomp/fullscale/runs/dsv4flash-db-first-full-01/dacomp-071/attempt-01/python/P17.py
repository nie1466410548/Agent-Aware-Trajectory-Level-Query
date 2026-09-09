import pandas as pd

# Get full data first
df_full = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, job_title, application_sources
FROM lever__opportunity_stage_history
"""))
df_full['stage_num'] = df_full['stage_id'].str.extract(r'(\d+)').astype(int)
df_full = df_full.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df_full['row_num'] = df_full.groupby('opportunity_id').cumcount()
df_full['n_rows'] = df_full.groupby('opportunity_id')['opportunity_id'].transform('count')
df_full['has_next'] = df_full['row_num'] < df_full['n_rows'] - 1
df_full['terminal'] = ~df_full['has_next']

# Now filter to Technical Assessment
ta = df_full[df_full['stage'] == 'Technical Assessment']
ta_attrited = ta[ta['terminal']]
ta_advanced = ta[~ta['terminal']]

print("=== TECHNICAL ASSESSMENT ===")
print(f"Total: {len(ta)}, Terminal/Attrited: {len(ta_attrited)}, Advanced: {len(ta_advanced)}")
print("Attrition reasons at Technical Assessment (terminal):")
print(ta_attrited['archive_reason'].value_counts().to_string())
print(f"\nAvg days - Attrited: {ta_attrited['days_in_stage'].mean():.1f}, Advanced: {ta_advanced['days_in_stage'].mean():.1f}")
print("\nBy job_team (attrited):")
print(ta_attrited.groupby('job_team').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).sort_values('cnt', ascending=False).to_string())

# Final Interview
fi = df_full[df_full['stage'] == 'Final Interview']
fi_attrited = fi[fi['terminal']]
fi_advanced = fi[~fi['terminal']]

print("\n=== FINAL INTERVIEW ===")
print(f"Total: {len(fi)}, Terminal/Attrited: {len(fi_attrited)}, Advanced: {len(fi_advanced)}")
print("Attrition reasons at Final Interview (terminal):")
print(fi_attrited['archive_reason'].value_counts().to_string())
print(f"\nAvg days - Attrited: {fi_attrited['days_in_stage'].mean():.1f}, Advanced: {fi_advanced['days_in_stage'].mean():.1f}")
print("\nBy job_team (attrited):")
print(fi_attrited.groupby('job_team').agg(cnt=('opportunity_id','count'), avg_days=('days_in_stage','mean')).sort_values('cnt', ascending=False).to_string())

# Days distribution
print("\n=== DAYS DISTRIBUTION ===")
for stage_name in ['Technical Assessment', 'Final Interview']:
    s = df_full[df_full['stage'] == stage_name]
    print(f"\n{stage_name}:")
    print(f"  Percentiles: 25th={s['days_in_stage'].quantile(0.25):.0f}, 50th={s['days_in_stage'].median():.0f}, 75th={s['days_in_stage'].quantile(0.75):.0f}")
    print(f"  90th={s['days_in_stage'].quantile(0.9):.0f}, 95th={s['days_in_stage'].quantile(0.95):.0f}")