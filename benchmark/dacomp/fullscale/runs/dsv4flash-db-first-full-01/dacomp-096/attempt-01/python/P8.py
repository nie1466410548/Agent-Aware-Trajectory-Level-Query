import json, pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Load data ----
cols_an = ["flow_id","flow_name","campaign_type","audience_bucket","created_at","updated_at","prev_updated_at",
          "hours_since_prev","or_calc","mu_or","sd_or","or_anomaly","ctor_calc","mu_ctor","sd_ctor",
          "ctor_anomaly","freq_anomaly","any_anomaly"]
rows_an = []
with open('/results/S16.rows.jsonl') as f:
    for line in f:
        rows_an.append(json.loads(line))
an = pd.DataFrame(rows_an, columns=cols_an)

# Parse dates
an['created_at'] = pd.to_datetime(an['created_at'])
an['hour'] = an['created_at'].dt.hour
an['weekday'] = an['created_at'].dt.dayofweek
an['is_weekend'] = an['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
an['daypart'] = an['hour'].apply(lambda x: 'Morning' if x < 12 else 'Afternoon')

# ---- Fig 1: Campaign Type Performance ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

type_agg = an.groupby('campaign_type').agg(
    mean_or=('or_calc','mean'), std_or=('or_calc','std'),
    mean_ctor=('ctor_calc','mean'), std_ctor=('ctor_calc','std'),
    n=('flow_id','count')
).reset_index()

colors = sns.color_palette("Set2", n_colors=8)
bars1 = ax1.bar(type_agg['campaign_type'], type_agg['mean_or'], yerr=type_agg['std_or'], 
                capsize=5, color=colors, edgecolor='gray')
ax1.set_ylabel('Open Rate')
ax1.set_title('Average Open Rate by Campaign Type', fontsize=13, fontweight='bold')
ax1.tick_params(axis='x', rotation=45)
for i, (v, bar) in enumerate(zip(type_agg['mean_or'], bars1)):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005, f'{v:.3f}', 
             ha='center', fontsize=9)

bars2 = ax2.bar(type_agg['campaign_type'], type_agg['mean_ctor'], yerr=type_agg['std_ctor'],
                capsize=5, color=colors, edgecolor='gray')
ax2.set_ylabel('Click-to-Open Rate')
ax2.set_title('Average Click-to-Open Rate by Campaign Type', fontsize=13, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
for i, (v, bar) in enumerate(zip(type_agg['mean_ctor'], bars2)):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.003, f'{v:.3f}',
             ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/campaign_type_performance.png', dpi=150)
plt.close()

# ---- Fig 2: Template Reuse vs Performance Scatter ----
cols20 = ["variation_id","campaign_type","n_uses","pct_of_type","avg_or","avg_ctor"]
rows20 = []
with open('/results/S20.rows.jsonl') as f:
    for line in f:
        rows20.append(json.loads(line))
tmpl = pd.DataFrame(rows20, columns=cols20)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors_t = sns.color_palette("husl", n_colors=len(tmpl['campaign_type'].unique()))
type_color_map = {t: c for t, c in zip(tmpl['campaign_type'].unique(), colors_t)}

for ct in tmpl['campaign_type'].unique():
    sub = tmpl[tmpl['campaign_type'] == ct]
    ax1.scatter(sub['n_uses'], sub['avg_or'], c=[type_color_map[ct]], label=ct, s=100, alpha=0.7, edgecolors='k')
ax1.set_xlabel('Number of Uses (Template Reuse)')
ax1.set_ylabel('Average Open Rate')
ax1.set_title('Template Reuse vs Open Rate', fontsize=13, fontweight='bold')
ax1.legend(fontsize=7, loc='best')

for ct in tmpl['campaign_type'].unique():
    sub = tmpl[tmpl['campaign_type'] == ct]
    ax2.scatter(sub['n_uses'], sub['avg_ctor'], c=[type_color_map[ct]], label=ct, s=100, alpha=0.7, edgecolors='k')
ax2.set_xlabel('Number of Uses (Template Reuse)')
ax2.set_ylabel('Average Click-to-Open Rate')
ax2.set_title('Template Reuse vs Click-to-Open Rate', fontsize=13, fontweight='bold')
ax2.legend(fontsize=7, loc='best')

plt.tight_layout()
plt.savefig('/work/template_reuse_performance.png', dpi=150)
plt.close()

# ---- Fig 3: Send Time Slot Performance ----
slot_agg = an.groupby(['is_weekend','daypart']).agg(
    mean_or=('or_calc','mean'), mean_ctor=('ctor_calc','mean'), n=('flow_id','count')
).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

pivot_or = slot_agg.pivot_table(index='is_weekend', columns='daypart', values='mean_or', aggfunc='mean')
sns.heatmap(pivot_or, annot=True, fmt='.4f', cmap='YlGn', ax=ax1, cbar_kws={'label': 'Open Rate'})
ax1.set_title('Open Rate by Send Time Slot', fontsize=12, fontweight='bold')

pivot_ctor = slot_agg.pivot_table(index='is_weekend', columns='daypart', values='mean_ctor', aggfunc='mean')
sns.heatmap(pivot_ctor, annot=True, fmt='.4f', cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'CTOR'})
ax2.set_title('Click-to-Open Rate by Send Time Slot', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/send_time_slot.png', dpi=150)
plt.close()

# ---- Fig 4: Near-Anomaly Campaigns ----
an['or_z'] = (an['or_calc'] - an['mu_or']) / an['sd_or']
an['ctor_z'] = (an['ctor_calc'] - an['mu_ctor']) / an['sd_ctor']
an['near_anomaly'] = (abs(an['or_z']) > 1.5) | (abs(an['ctor_z']) > 1.5)

fig, ax = plt.subplots(figsize=(12, 6))

for ct in an['campaign_type'].unique():
    sub = an[an['campaign_type'] == ct]
    ax.scatter(sub['or_calc'], sub['ctor_calc'], c=[type_color_map[ct]], label=ct, s=60, alpha=0.6, edgecolors='gray')

# Highlight near-anomalies
near_an = an[an['near_anomaly']]
ax.scatter(near_an['or_calc'], near_an['ctor_calc'], c='red', s=120, marker='X', 
           label='Near-Anomaly (|z|>1.5)', alpha=0.9, edgecolors='darkred', linewidth=1.5)

# Add labels for near-anomalies
for _, row in near_an.iterrows():
    ax.annotate(row['flow_id'].replace('FLOW-',''), (row['or_calc'], row['ctor_calc']),
                fontsize=8, fontweight='bold')

ax.set_xlabel('Open Rate')
ax.set_ylabel('Click-to-Open Rate')
ax.set_title('Campaign Performance: Near-Anomaly Detection', fontsize=13, fontweight='bold')
ax.legend(fontsize=8, loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/near_anomaly_scatter.png', dpi=150)
plt.close()

print("All figures saved.")
print(f"Files: /work/campaign_type_performance.png, /work/template_reuse_performance.png, /work/send_time_slot.png, /work/near_anomaly_scatter.png")