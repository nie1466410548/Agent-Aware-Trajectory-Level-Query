import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style('whitegrid')
os.makedirs('/work', exist_ok=True)

# ============ DATA ============
channels = pd.DataFrame({
    'channel': ['email', 'sms', 'web', 'mobile', 'social'],
    'surveys_using_channel': [734, 648, 484, 431, 57],
    'total_responses': [1207, 1058, 679, 544, 92],
    'completed_responses': [610, 552, 280, 171, 40],
    'unique_participants': [1025, 899, 577, 462, 78],
    'completion_rate': [0.505, 0.523, 0.413, 0.316, 0.437],
    'efficiency_score': [72.99, 60.11, 63.68, 46.58, 41.94],
    'market_share': [0.35, 0.25, 0.22, 0.18, 0.08],
    'tier': ['Tier 1 - Premium', 'Tier 1 - Premium', 'Tier 2 - Standard', 'Tier 2 - Standard', 'Tier 3 - Experimental']
})

# Final allocation (robust average from sensitivity analysis)
final_share = {'email': 0.303, 'sms': 0.370, 'web': 0.200, 'mobile': 0.098, 'social': 0.030}
channels['final_share'] = channels['channel'].map(final_share)
channels['yield'] = channels['completed_responses'] / (channels['market_share'] * 100)
channels['forecast'] = channels['final_share'] * 100 * channels['yield']
channels['change'] = channels['final_share'] - channels['market_share']

current_total = channels['completed_responses'].sum()
forecast_total = channels['forecast'].sum()
uplift = (forecast_total - current_total) / current_total * 100

# ============ FIG 1: Channel performance matrix ============
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Left: completion vs efficiency bubble
ax = axes[0]
for i, row in channels.iterrows():
    size = row['market_share'] * 1800
    ax.scatter(row['completion_rate'], row['efficiency_score'], s=size, alpha=0.75,
               edgecolors='black', linewidth=1.5, color=plt.cm.tab10(i))
    ax.annotate(row['channel'].upper(), (row['completion_rate'], row['efficiency_score']),
                textcoords='offset points', xytext=(6, 6), fontsize=10, fontweight='bold')
ax.set_xlabel('Completion Rate', fontsize=12)
ax.set_ylabel('Efficiency Score', fontsize=12)
ax.set_title('(a) Channel Performance: Completion vs Efficiency\n(Bubble size = current budget share)', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)

# Right: user value & robustness
ax = axes[1]
user_val = {'email': 1.0405, 'sms': 1.1718, 'web': 0.978, 'mobile': 0.610, 'social': 1.111}
robust = {'email': 0.959, 'sms': 0.912, 'web': 0.962, 'mobile': 0.962, 'social': 0.089}
channels['user_val'] = channels['channel'].map(user_val)
channels['robust'] = channels['channel'].map(robust)
x = np.arange(5)
w = 0.38
ax.bar(x - w/2, channels['user_val'], w, label='User Lifecycle Value Factor', color='#2E86AB', edgecolor='black')
ax.bar(x + w/2, channels['robust'], w, label='Category Robustness (1-CV)', color='#6A994E', edgecolor='black')
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=10)
ax.set_ylabel('Factor (relative to all-user average = 1.0)', fontsize=11)
ax.set_title('(b) User Value & Category Consistency\n(Contact LTV & Survey category completion)', fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='upper left')
ax.set_ylim(0, 1.3)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig_final_1_channel_profile.png', dpi=150)
plt.close()

# ============ FIG 2: Category heatmap ============
cat_comp = {
    'email': [0.578, 0.607, 0.639],
    'sms': [0.527, 0.425, 0.491],
    'web': [0.410, 0.379, 0.378],
    'mobile': [0.410, 0.379, 0.378],
    'social': [0.167, 0.012, 0.042]
}
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Heatmap
ax = axes[0]
mat = np.array([cat_comp[ch] for ch in ['email', 'sms', 'web', 'mobile', 'social']])
sns.heatmap(mat, annot=True, fmt='.0%', cmap='RdYlGn', ax=ax,
            xticklabels=['Evaluation', 'Feedback', 'Research'],
            yticklabels=['EMAIL', 'SMS', 'WEB', 'MOBILE', 'SOCIAL'],
            linewidths=1.5, cbar_kws={'label': 'Completion Rate'}, vmin=0, vmax=0.7)
ax.set_title('(a) Completion Rate by Channel × Project Category', fontsize=13, fontweight='bold')

# Mix bar (channel response volume share by category)
ax = axes[1]
cat_mix = {
    'email': [0.079, 0.314, 0.607],
    'sms': [0.528, 0.153, 0.319],
    'web': [0.196, 0.508, 0.296],
    'mobile': [0.196, 0.508, 0.296],
    'social': [0.507, 0.119, 0.374]
}
bottoms = np.zeros(5)
labels = ['Evaluation', 'Feedback', 'Research']
colors = ['#C73E1D', '#F18F01', '#2E86AB']
for j, cat in enumerate(labels):
    vals = np.array([cat_mix[ch][j] for ch in ['email', 'sms', 'web', 'mobile', 'social']])
    ax.bar(range(5), vals, bottom=bottoms, color=colors[j], label=cat, edgecolor='black', linewidth=0.8)
    bottoms += vals
ax.set_xticks(range(5))
ax.set_xticklabels(['EMAIL', 'SMS', 'WEB', 'MOBILE', 'SOCIAL'], fontsize=10)
ax.set_ylabel('Share of channel responses (%)', fontsize=11)
ax.set_title('(b) Project Category Mix per Channel\n(Survey table, response volume)', fontsize=13, fontweight='bold')
ax.legend(fontsize=9, title='Category')
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(plt.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig('/work/fig_final_2_category.png', dpi=150)
plt.close()

# ============ FIG 3: Cohort value distribution ============
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
cohort_data = [
    ('All Users', [0.0, 0.46, 18.32, 81.21]),
    ('Email-Reached Users', [0.0, 0.99, 19.14, 79.87]),
    ('SMS-Reached Users', [0.0, 2.99, 20.87, 76.14])
]
for ax, (title, shares) in zip(axes, cohort_data):
    bars = ax.bar(['Q1\n(Bottom)', 'Q2', 'Q3', 'Q4\n(Top)'], shares,
                  color=['#D0D0D0', '#9A9A9A', '#5A5A5A', '#2E86AB'], edgecolor='black', linewidth=1.2)
    for bar, val in zip(bars, shares):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, f'{val:.1f}%',
                ha='center', fontsize=10, fontweight='bold')
    ax.set_title(f'{title}\nLifecycle Value by Cohort', fontsize=12, fontweight='bold')
    ax.set_ylabel('% of Total Lifecycle Value', fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig_final_3_cohorts.png', dpi=150)
plt.close()

# ============ FIG 4: Budget reallocation ============
fig, ax = plt.subplots(figsize=(11, 6.5))
x = np.arange(5)
w = 0.38
bars1 = ax.bar(x - w/2, channels['market_share']*100, w, label='Current Budget Share', color='#B0B0B0', edgecolor='black')
bars2 = ax.bar(x + w/2, channels['final_share']*100, w, label='Optimal Investment Ratio', color='#2E86AB', edgecolor='black')
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f'{bar.get_height():.1f}%',
            ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f'{bar.get_height():.1f}%',
            ha='center', fontsize=9, fontweight='bold', color='#2E86AB')
# Delta arrows
for i, row in channels.iterrows():
    delta = (row['final_share'] - row['market_share']) * 100
    if abs(delta) > 0.3:
        y_top = max(row['market_share'], row['final_share']) * 100 + 5
        ax.annotate(f'{delta:+.1f} pts', (i, y_top), ha='center', fontsize=9, fontweight='bold',
                    color='#C73E1D' if delta > 0 else '#1B4965')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11, fontweight='bold')
ax.set_ylabel('Share of Total Budget (%)', fontsize=12)
ax.set_title('Recommended Channel Budget Reallocation Plan', fontsize=15, fontweight='bold')
ax.legend(fontsize=10)
ax.set_ylim(0, 55)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig_final_4_reallocation.png', dpi=150)
plt.close()

# ============ FIG 5: Forecast ============
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

ax = axes[0]
x = np.arange(5)
w = 0.38
bars1 = ax.bar(x - w/2, channels['completed_responses'], w, label='Current Completed Responses', color='#B0B0B0', edgecolor='black')
bars2 = ax.bar(x + w/2, channels['forecast'], w, label='Forecast Completed Responses', color='#2E86AB', edgecolor='black')
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, f'{int(bar.get_height())}', ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, f'{int(bar.get_height())}', ha='center', fontsize=9, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=10, fontweight='bold')
ax.set_ylabel('Completed Responses', fontsize=11)
ax.set_title('(a) Forecast of Expected Returns by Channel', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
vals = [current_total, forecast_total]
bars = ax.bar(['Current Portfolio', 'Forecast Portfolio'], vals,
              color=['#B0B0B0', '#2E86AB'], edgecolor='black', width=0.5)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f'{val:.0f}\n({val/current_total*100:.1f}% of current)',
            ha='center', fontsize=11, fontweight='bold')
ax.set_ylabel('Total Completed Responses', fontsize=11)
ax.set_title(f'(b) Portfolio-Level Return\nNet uplift: +{uplift:.1f}%', fontsize=13, fontweight='bold')
ax.set_ylim(0, forecast_total * 1.25)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig_final_5_forecast.png', dpi=150)
plt.close()

# ============ FIG 6: Contact funnel & lifecycle ============
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

ax = axes[0]
funnel = pd.DataFrame({
    'metric': ['Open Rate', 'Start Rate', 'Complete Rate'],
    'email': [0.646, 0.366, 0.116],
    'sms': [0.667, 0.432, 0.152]
})
x = np.arange(3)
w = 0.35
ax.bar(x - w/2, funnel['email'], w, label='Email', color='#2E86AB', edgecolor='black')
ax.bar(x + w/2, funnel['sms'], w, label='SMS', color='#A23B72', edgecolor='black')
for xi, (e, s) in enumerate(zip(funnel['email'], funnel['sms'])):
    ax.text(xi - w/2, e + 0.01, f'{e:.1%}', ha='center', fontsize=9)
    ax.text(xi + w/2, s + 0.01, f'{s:.1%}', ha='center', fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(funnel['metric'], fontsize=11)
ax.set_ylabel('Rate (per contact)', fontsize=11)
ax.set_title('(a) Contact-Level Engagement Funnel\n(Email vs SMS, contact table)', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(0, 0.8)
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
groups = ['Both\nEmail+SMS', 'Email\nOnly', 'SMS\nOnly', 'Neither']
users = [3309, 532, 86, 73]
ltv = [4.227, 0.145, 0.140, 0.0]
bars = ax.bar(groups, ltv, color=['#2E86AB', '#6A994E', '#A23B72', '#C0C0C0'], edgecolor='black', linewidth=1.2)
for bar, u, v in zip(bars, users, ltv):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'LTV {v:.2f}\n(n={u})',
            ha='center', fontsize=9, fontweight='bold')
ax.set_ylabel('Avg Lifecycle Completed Surveys', fontsize=11)
ax.set_title('(b) User Lifecycle Value by Channel Engagement\n(Contact table)', fontsize=12, fontweight='bold')
ax.set_ylim(0, 5)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig_final_6_contact.png', dpi=150)
plt.close()

print("Figures saved:")
for f in sorted(os.listdir('/work')):
    print(' ', f)

print(f"\nCurrent total completed: {current_total}")
print(f"Forecast total completed: {forecast_total:.1f}")
print(f"Uplift: {uplift:+.1f}%")
print("\nFinal allocation table:")
print(channels[['channel', 'tier', 'market_share', 'final_share', 'completed_responses', 'forecast', 'yield']].to_string(index=False))