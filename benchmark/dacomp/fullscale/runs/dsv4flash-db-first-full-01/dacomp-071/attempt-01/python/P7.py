import pandas as pd

df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)

# For each opportunity, find the max stage_num reached
opp_max = df.groupby('opportunity_id')['stage_num'].max().reset_index()
opp_max.columns = ['opportunity_id', 'max_stage_num']

# Merge
df = df.merge(opp_max, on='opportunity_id')

# Define pass_like reasons
pass_reasons = ['Advanced to next stage', 'Qualified', 'Proceeding', 'Hired']

# For each stage, compute metrics
results = []
for stage_num, grp in df.groupby('stage_num'):
    stage_name = grp['stage'].iloc[0]
    stage_id = grp['stage_id'].iloc[0]
    total = len(grp)
    avg_days = grp['days_in_stage'].mean()
    
    # Advanced: has a later stage record
    advanced = (grp['max_stage_num'] > stage_num).sum()
    
    # Terminal at this stage: max_stage_num == stage_num
    terminal = grp[grp['max_stage_num'] == stage_num]
    attrited = len(terminal[~terminal['archive_reason'].isin(pass_reasons)])
    proceeding = len(terminal[terminal['archive_reason'] == 'Proceeding'])
    hired = len(terminal[terminal['archive_reason'] == 'Hired'])
    qualified_or_advanced = len(terminal[terminal['archive_reason'].isin(['Advanced to next stage', 'Qualified'])])
    
    # Among resolved (not proceeding)
    resolved = total - proceeding
    if resolved > 0:
        pass_rate = advanced / resolved
        attrition_rate = attrited / resolved
    else:
        pass_rate = 0
        attrition_rate = 0
    
    # Efficiency index = pass_rate / avg_days * 100
    eff_index = pass_rate / avg_days * 100 if avg_days > 0 else 0
    
    results.append({
        'stage_num': stage_num,
        'stage_id': stage_id,
        'stage': stage_name,
        'total_entries': total,
        'avg_days': round(avg_days, 1),
        'advanced': advanced,
        'attrited': attrited,
        'proceeding': proceeding,
        'hired': hired,
        'pass_rate_pct': round(pass_rate * 100, 1),
        'attrition_rate_pct': round(attrition_rate * 100, 1),
        'eff_index': round(eff_index, 2)
    })

res_df = pd.DataFrame(results)
print(res_df.to_string(index=False))