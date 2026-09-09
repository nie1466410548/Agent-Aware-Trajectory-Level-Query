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

metrics = []
for st, grp in df.groupby('stage_num'):
    total = len(grp)
    avg_days = grp['days_in_stage'].mean()
    advanced = grp['has_next'].sum()
    stage_name = grp['stage'].iloc[0]
    pass_rate = advanced / total
    attrited = total - advanced if stage_name != 'Hired' else 0
    attrition_rate = attrited / total if stage_name != 'Hired' else 0.0
    eff_index = pass_rate / avg_days * 100 if stage_name != 'Hired' else np.nan
    metrics.append({
        'stage_num': st, 'stage': stage_name, 'total_entries': total,
        'avg_days': round(avg_days, 1), 'advanced': advanced,
        'attrited': attrited, 'pass_rate_pct': round(pass_rate*100,1),
        'attrition_rate_pct': round(attrition_rate*100,1),
        'eff_index': round(eff_index, 2) if not np.isnan(eff_index) else None
    })
m = pd.DataFrame(metrics)
m = m[m['stage'] != 'Hired']
m = m.sort_values('stage_num')

plt.rcParams.update({'font.size': 10})
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
stages = m['stage'].tolist()
x = np.arange(len(stages))

axes[0].bar(x, m['avg_days'], color=['#d62728' if (a>25) else '#1f77b4' for a in m['avg_days']])
axes[0].axhline(25, color='red', ls='--', lw=1.2)
axes[0].set_xticks(x); axes[0].set_xticklabels(stages, rotation=45, ha='right')
axes[0].set_title('Average Days in Stage (red = > 25 days)')
axes[0].set_ylabel('Avg days')
for i, v in enumerate(m['avg_days']): axes[0].text(i, v+1, str(v), ha='center', fontsize=8)

axes[1].bar(x, m['attrition_rate_pct'], color=['#d62728' if (a>40) else '#1f77b4' for a in m['attrition_rate_pct']])
axes[1].axhline(40, color='red', ls='--', lw=1.2)
axes[1].set_xticks(x); axes[1].set_xticklabels(stages, rotation=45, ha='right')
axes[1].set_title('Attrition Rate % (red = > 40%)')
axes[1].set_ylabel('%')
for i, v in enumerate(m['attrition_rate_pct']): axes[1].text(i, v+1, str(v), ha='center', fontsize=8)

effs = m['eff_index']
axes[2].bar(x, effs, color=['#d62728' if (e<1.5) else '#1f77b4' for e in effs])
axes[2].axhline(1.5, color='red', ls='--', lw=1.2)
axes[2].set_xticks(x); axes[2].set_xticklabels(stages, rotation=45, ha='right')
axes[2].set_title('Efficiency Index (pass_rate/avg_days*100, red = < 1.5)')
axes[2].set_ylabel('Efficiency index')
for i, v in enumerate(effs): axes[2].text(i, v+0.05, str(v), ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('stage_bottleneck_analysis.png', dpi=120)
print("Saved stage_bottleneck_analysis.png")
print(m[['stage','total_entries','avg_days','pass_rate_pct','attrition_rate_pct','eff_index']].to_string(index=False))
