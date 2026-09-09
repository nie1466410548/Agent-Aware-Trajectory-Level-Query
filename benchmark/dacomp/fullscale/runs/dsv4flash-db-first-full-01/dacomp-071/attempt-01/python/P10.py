import pandas as pd

df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

pass_reasons = ['Advanced to next stage', 'Qualified', 'Proceeding', 'Hired']
df['pass_like'] = df['archive_reason'].isin(pass_reasons)

rows = []
for st, grp in df.groupby('stage_num'):
    total = len(grp)
    avg_days = grp['days_in_stage'].mean()
    # Definition A: pass = has later stage record
    passA = grp['has_next'].sum()
    attA = total - passA - grp['archive_reason'].eq('Hired').sum()
    # Definition B: pass = pass_like archive_reason
    passB = grp['pass_like'].sum()
    attB = total - passB
    rows.append({
        'stage_num': st, 'stage': grp['stage'].iloc[0], 'total': total, 'avg_days': round(avg_days,1),
        'passA_pct': round(passA/total*100,1), 'attA_pct': round(attA/total*100,1),
        'passB_pct': round(passB/total*100,1), 'attB_pct': round(attB/total*100,1),
        'effA': round((passA/total)/avg_days*100, 2), 'effB': round((passB/total)/avg_days*100, 2),
        'pass_like_cnt': passB, 'attrition_reason_cnt': attB
    })
r = pd.DataFrame(rows)
print(r.to_string(index=False))
