import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df_all = pd.read_csv('/work/df_all.csv')
df_all['is_problem'] = df_all['is_problem'].astype(int)
df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

sns.set_style('whitegrid')
plt.rcParams.update({'figure.dpi': 110, 'font.size': 9})

# Fig 1: CTR vs CVR scatter
fig, ax = plt.subplots(figsize=(7,5))
colors = {0:'#4C72B0', 1:'#C44E52'}
labels = {0:'Normal ad groups (n=4053)', 1:'Problem ad groups (n=271)'}
for g in [0,1]:
    sub = df_all[df_all['is_problem']==g]
    ax.scatter(sub['ctr']*100, sub['cvr']*100, s=12, alpha=0.55, color=colors[g], label=labels[g])
ax.axvline(3.5874, color='grey', ls='--', lw=1)
ax.axhline(3.846, color='grey', ls='--', lw=1)
ax.text(3.68, 22, 'CTR P75 = 3.59%', rotation=90, fontsize=8, color='grey')
ax.text(1.2, 3.95, 'CVR P25 = 3.85%', fontsize=8, color='grey')
ax.set_xlabel('CTR (%)'); ax.set_ylabel('Conversion rate (%)')
ax.set_title('Ad group CTR vs Conversion Rate (problem quadrant = top-left)')
ax.legend(loc='upper right', fontsize=8)
plt.tight_layout(); plt.savefig('/work/fig1_scatter.png'); plt.close()

# Fig 2: Box plots of IMI and TQS
fig, axes = plt.subplots(1, 2, figsize=(10,4))
df_all['Group'] = np.where(df_all['is_problem']==1, 'Problem', 'Normal')
sns.boxplot(data=df_all[df_all['intent_match_index'].notna()], x='Group', y='intent_match_index', ax=axes[0], palette=['#4C72B0','#C44E52'])
axes[0].axhline(1.0, color='grey', ls='--', lw=1); axes[0].set_title('Intent Match Index (actual/expected CVR)')
axes[0].set_ylabel('IMI'); axes[0].set_ylim(0, 4)
sns.boxplot(data=df_all, x='Group', y='traffic_quality_score', ax=axes[1], palette=['#4C72B0','#C44E52'])
axes[1].set_title('Traffic Quality Score'); axes[1].set_ylabel('TQS (0-100)')
plt.tight_layout(); plt.savefig('/work/fig2_boxes.png'); plt.close()

# Fig 3: Channel x Strategy problem rates
df_all['channel_strategy'] = df_all['channel'] + ' / ' + df_all['strategy']
ct = df_all.groupby('channel_strategy').agg(total=('ad_group_id','count'), problem=('is_problem','sum')).reset_index()
ct['problem_pct'] = 100.0*ct['problem']/ct['total']
ct = ct.sort_values('problem_pct', ascending=True)
fig, ax = plt.subplots(figsize=(8,7))
bars = ax.barh(ct['channel_strategy'], ct['problem_pct'], color=np.where(ct['problem_pct']>=7.5, '#C44E52', '#4C72B0'))
ax.axvline(100.0*271/4324, color='grey', ls='--', lw=1)
ax.text(6.7, 24.5, 'Overall avg 6.3%', fontsize=8, color='grey')
ax.set_xlabel('Problem ad-group share (%)'); ax.set_title('Problem ad-group share by Channel / Strategy')
plt.tight_layout(); plt.savefig('/work/fig3_channels.png'); plt.close()

# Fig 4: Seasonality
period_stats = df_all.groupby('period').agg(total=('ad_group_id','count'), problem=('is_problem','sum')).reset_index()
period_stats['problem_pct'] = 100.0*period_stats['problem']/period_stats['total']
period_stats = period_stats.sort_values('problem_pct', ascending=False)
fig, ax = plt.subplots(figsize=(8,4.5))
ax.bar(period_stats['period'], period_stats['problem_pct'], color='#C44E52' if period_stats['problem_pct'].max() else '#4C72B0')
ax.bar(period_stats['period'], period_stats['problem_pct'], color=np.where(period_stats['problem_pct']>=7.5, '#C44E52', '#4C72B0'))
ax.axhline(6.27, color='grey', ls='--', lw=1)
ax.set_xticklabels(period_stats['period'], rotation=45, ha='right')
ax.set_ylabel('Problem ad-group share (%)'); ax.set_title('Problem ad-group share by campaign period (Q4/Holiday elevated)')
plt.tight_layout(); plt.savefig('/work/fig4_periods.png'); plt.close()

print("Figures saved.")