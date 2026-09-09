import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

# Per-stage metrics
metrics = []
for st, grp in df.groupby('stage_num'):
    total = len(grp)
    avg_days = grp['days_in_stage'].mean()
    std_days = grp['days_in_stage'].std()
    med_days = grp['days_in_stage'].median()
    advanced = grp['has_next'].sum()
    pass_rate = advanced / total
    attrition_rate = 1 - pass_rate
    
    # Exclude Hired stage for efficiency (terminal)
    if stage == 'Hired':
        eff_index = 0
    else:
        eff_index = pass_rate / avg_days * 100
    
    # Also compute by archive_reason definition for reference
    pass_reasons = ['Advanced to next stage', 'Qualified', 'Proceeding', 'Hired']
    pass_by_reason = grp['archive_reason'].isin(pass_reasons).sum()
    
    metrics.append({
        'stage_num': st,
        'stage_id': grp['stage_id'].iloc[0],
        'stage': grp['stage'].iloc[0],
        'total_entries': total,
        'avg_days': round(avg_days, 1),
        'std_days': round(std_days, 1),
        'med_days': med_days,
        'min_days': grp['days_in_stage'].min(),
        'max_days': grp['days_in_stage'].max(),
        'advanced': advanced,
        'attrited': total - advanced - (1 if grp['stage'].iloc[0]=='Hired' else 0),
        'pass_rate_pct': round(pass_rate * 100, 1),
        'attrition_rate_pct': round(attrition_rate * 100, 1),
        'eff_index': round(eff_index, 2),
        'pass_by_reason_pct': round(pass_by_reason / total * 100, 1)
    })

m = pd.DataFrame(metrics)
print(m.to_string(index=False))

# Identify bottlenecks
print("\n=== BOTTLENECK STAGES (avg_days > 25 AND attrition > 40%) ===")
bottlenecks = m[(m['avg_days'] > 25) & (m['attrition_rate_pct'] > 40)]
print(bottlenecks[['stage','total_entries','avg_days','attrition_rate_pct','eff_index']].to_string(index=False))

print("\n=== STAGES WITH EFFICIENCY INDEX < 1.5 (at least 100 samples) ===")
low_eff = m[(m['eff_index'] < 1.5) & (m['total_entries'] >= 100)]
print(low_eff[['stage','total_entries','avg_days','attrition_rate_pct','pass_rate_pct','eff_index']].to_string(index=False))

print("\n=== ALL STAGES WITH EFFICIENCY INDEX < 1.5 ===")
print(m[m['eff_index'] < 1.5][['stage','total_entries','avg_days','attrition_rate_pct','eff_index']].to_string(index=False))