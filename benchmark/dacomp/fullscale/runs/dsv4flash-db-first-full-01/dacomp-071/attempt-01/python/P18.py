import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create a funnel visualization
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
    metrics.append({'stage_num': st, 'stage': stage_name, 'total_entries': total,
                    'avg_days': round(avg_days, 1), 'advanced': advanced,
                    'attrited': attrited, 'pass_rate': round(pass_rate*100,1),
                    'attrition_rate': round(attrition_rate*100,1),
                    'eff_index': round(eff_index, 2) if not np.isnan(eff_index) else None})
m = pd.DataFrame(metrics)

# Funnel plot
fig, ax = plt.subplots(figsize=(10, 6))
stages = m['stage'].tolist()
vals = m['total_entries'].tolist()
colors = ['#d62728' if s in ['Technical Assessment','Final Interview'] else '#1f77b4' for s in stages]
ax.barh(range(len(stages)), vals, color=colors, height=0.6)
ax.set_yticks(range(len(stages)))
ax.set_yticklabels(stages)
ax.set_xlabel('Number of candidates entering stage')
ax.set_title('Hiring Funnel: Candidate Count per Stage\n(Bottleneck stages in red)')
for i, (v, s) in enumerate(zip(vals, stages)):
    ax.text(v+10, i, f'{v} ({m.iloc[i]["attrition_rate"]}% attrit)', va='center', fontsize=9)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('funnel_visualization.png', dpi=120)
print("Saved funnel_visualization.png")

# Also create a simple table for the report
print("\n\n=== FINAL METRICS TABLE ===")
print(m.to_string(index=False))