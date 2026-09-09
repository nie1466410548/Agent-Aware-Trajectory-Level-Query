
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/user_level.csv')

sns.set_theme(style='whitegrid', context='talk')
pal = {'single_feature': '#d62728', 'other': '#1f77b4'}
order = ['single_feature', 'other']
labels = {'single_feature': 'Single-feature heavy\n(>60 active days, <5 features)', 'other': 'Other users'}

# ---- Figure 1: average_daily_minutes distribution ----
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
sns.kdeplot(data=df[df['segment']=='single_feature']['average_daily_minutes'], label='Single-feature heavy', color='#d62728', fill=True, ax=axes[0])
sns.kdeplot(data=df[df['segment']=='other']['average_daily_minutes'], label='Other users', color='#1f77b4', fill=True, ax=axes[0])
axes[0].axvline(32.47, color='#d62728', ls='--', lw=1.2)
axes[0].axvline(60.90, color='#1f77b4', ls='--', lw=1.2)
axes[0].set_title('Average daily minutes')
axes[0].set_xlabel('average_daily_minutes')

sns.boxplot(data=df, x='segment', y='average_daily_minutes', order=order, palette=pal, ax=axes[1])
axes[1].set_xticklabels([labels[s] for s in order], fontsize=9)
axes[1].set_title('Box: average daily minutes')
plt.tight_layout()
plt.savefig('/work/fig1_daily_minutes.png', dpi=110)
plt.close()

# ---- Figure 2: NPS distribution ----
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
for s in order:
    sns.kdeplot(data=df[df['segment']==s]['latest_nps_rating'], label=labels[s], fill=True, ax=axes[0], color=pal[s])
axes[0].set_title('NPS rating distribution')
axes[0].set_xlabel('latest_nps_rating')
sns.boxplot(data=df, x='segment', y='latest_nps_rating', order=order, palette=pal, ax=axes[1])
axes[1].set_xticklabels([labels[s] for s in order], fontsize=9)
axes[1].set_title('Box: NPS rating')
plt.tight_layout()
plt.savefig('/work/fig2_nps.png', dpi=110)
plt.close()

# ---- Figure 3: retention metrics ----
ret = df.groupby('segment')[['count_active_days','count_active_months']].mean().loc[order]
span = (pd.to_datetime(df['last_event_on']) - pd.to_datetime(df['first_event_on'])).dt.days
df['tenure_days'] = span
ret['tenure_days'] = df.groupby('segment')['tenure_days'].mean().loc[order]
fig, ax = plt.subplots(figsize=(10, 5.5))
ret.T.plot(kind='bar', color=['#d62728','#1f77b4'], ax=ax)
ax.set_title('Engagement longevity (retention proxies)')
ax.set_ylabel('Mean')
ax.set_xticklabels(['Active days','Active months','Tenure days'], rotation=0)
ax.legend(title='Segment', labels=['Single-feature heavy','Other users'])
plt.tight_layout()
plt.savefig('/work/fig3_retention.png', dpi=110)
plt.close()

# ---- Figure 4: top features ----
fcols = ["visitor_id","feature_id","feature_name","product_area_name","page_name","app_display_name","sum_clicks","sum_minutes","avg_daily_minutes","count_click_events"]
frows = []
with open('/results/S35.rows.jsonl') as f:
    for line in f:
        frows.append(json.loads(line))
feat = pd.DataFrame(frows, columns=fcols)

# Top features by number of single-feature users
top_feats = feat.groupby('feature_name').agg(
    n_users=('visitor_id','nunique'),
    total_clicks=('sum_clicks','sum')).reset_index().sort_values('n_users', ascending=False).head(12)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_feats, x='n_users', y='feature_name', color='#d62728', ax=ax)
ax.set_title('Top 12 features used by single-feature-heavy users')
ax.set_xlabel('Number of single-feature users')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('/work/fig4_top_features.png', dpi=110)
plt.close()

# ---- Figure 5: product area mix ----
pa = feat.groupby('product_area_name').agg(n_users=('visitor_id','nunique')).reset_index().sort_values('n_users', ascending=False)
fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(data=pa, x='n_users', y='product_area_name', palette='rocket_r', ax=ax)
ax.set_title('Product areas touched by single-feature-heavy users')
ax.set_xlabel('Number of single-feature users')
plt.tight_layout()
plt.savefig('/work/fig5_product_areas.png', dpi=110)
plt.close()

# ---- Figure 6: dominant-feature concentration ----
user_tot = feat.groupby('visitor_id')['sum_clicks'].sum().rename('total_clicks')
user_max = feat.groupby('visitor_id')['sum_clicks'].max().rename('max_clicks')
con = pd.concat([user_tot, user_max], axis=1)
con['dominant_share'] = con['max_clicks'] / con['total_clicks']
con['n_features'] = feat.groupby('visitor_id')['feature_id'].nunique()
fig, ax = plt.subplots(figsize=(10, 5.5))
con.groupby('n_features')['dominant_share'].mean().plot(kind='bar', color='#d62728', ax=ax)
ax.set_title('Dominant-feature click concentration by feature count')
ax.set_xlabel('Distinct features used')
ax.set_ylabel('Avg share of clicks on top feature')
ax.set_ylim(0, 1.05)
for i, v in enumerate(con.groupby('n_features')['dominant_share'].mean().values):
    ax.text(i, v+0.02, f'{v:.2f}', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('/work/fig6_concentration.png', dpi=110)
plt.close()

print("Figures saved.")
print("Feat shape:", feat.shape)
print(top_feats.to_string(index=False))
