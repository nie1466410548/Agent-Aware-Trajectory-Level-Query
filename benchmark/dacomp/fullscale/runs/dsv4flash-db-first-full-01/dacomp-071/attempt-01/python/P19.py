import pandas as pd

df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, application_sources
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1
df['terminal'] = ~df['has_next']

# Data quality issue: negative reason but advanced
pass_reasons = ['Advanced to next stage','Qualified','Proceeding','Hired']
neg_advanced = df[(df['has_next']) & (~df['archive_reason'].isin(pass_reasons))]
print("Data quality: negative archive_reason but candidate advanced ->", len(neg_advanced))
print(neg_advanced.groupby('stage').size().to_string())

# Attrition reason breakdown for bottleneck stages (terminal only)
for stg in ['Technical Assessment', 'Final Interview']:
    sub = df[(df['stage'] == stg) & (df['terminal'])]
    total_att = len(sub)
    print(f"\n{stg} attrition reasons (n={total_att}):")
    vc = sub['archive_reason'].value_counts()
    for reason, cnt in vc.items():
        print(f"  {reason}: {cnt} ({cnt/total_att*100:.1f}%)")
    # team-level attrition rates
    all_sub = df[df['stage'] == stg]
    team_tbl = all_sub.groupby('job_team').apply(
        lambda g: pd.Series({'entered': len(g), 'attrited': g['terminal'].sum(),
                             'att_rate': round(g['terminal'].mean()*100,1),
                             'avg_days': round(g['days_in_stage'].mean(),1)}),
        include_groups=False).reset_index()
    print(f"\n  {stg} by team:")
    print(team_tbl.sort_values('att_rate', ascending=False).to_string(index=False))
