import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Load model
channels = pd.read_csv('/work/channel_model.csv')

# Survey-level category mix per channel (from query results)
# Channel response distribution across categories
cat_mix = {
    'email': {'evaluation': 0.079, 'feedback': 0.314, 'research': 0.607},
    'sms': {'evaluation': 0.528, 'feedback': 0.153, 'research': 0.319},
    'web': {'evaluation': 0.196, 'feedback': 0.508, 'research': 0.296},
    'mobile': {'evaluation': 0.196, 'feedback': 0.508, 'research': 0.296},
    'social': {'evaluation': 0.507, 'feedback': 0.119, 'research': 0.374}
}

# Channel completion rates by category (from survey table)
cat_comp = {
    'email': {'evaluation': 0.578, 'feedback': 0.607, 'research': 0.639},
    'sms': {'evaluation': 0.527, 'feedback': 0.425, 'research': 0.491},
    'web': {'evaluation': 0.410, 'feedback': 0.379, 'research': 0.378},
    'mobile': {'evaluation': 0.410, 'feedback': 0.379, 'research': 0.378},
    'social': {'evaluation': 0.167, 'feedback': 0.012, 'research': 0.042}
}

# Compute weighted completion rate per channel (using category mix)
# This is the expected completion rate given the category mix of each channel
print("=== WEIGHTED COMPLETION RATE (Survey-based) ===")
for ch in channels['channel']:
    weighted = sum(cat_mix[ch][cat] * cat_comp[ch][cat] for cat in ['evaluation', 'feedback', 'research'])
    print(f"{ch:>8}: {weighted:.1%}")

# Forecast by category under new allocation
# Current completed by category × channel (from survey table)
cat_current = {
    'evaluation': {'email': 2840, 'sms': 6949, 'social': 298, 'web_mobile': 6485},
    'feedback': {'email': 11870, 'sms': 1627, 'social': 5, 'web_mobile': 15559},
    'research': {'email': 24183, 'sms': 3899, 'social': 56, 'web_mobile': 9052}
}
# Map web_mobile to web and mobile
cat_current_detail = {}
for cat, ch_data in cat_current.items():
    total_wm = ch_data['web_mobile']
    # Split web_mobile by response ratio from channel_performance
    web_share = 679 / (679 + 544)  # 0.555
    mobile_share = 544 / (679 + 544)  # 0.445
    cat_current_detail[cat] = {
        'email': ch_data['email'],
        'sms': ch_data['sms'],
        'social': ch_data['social'],
        'web': int(total_wm * web_share),
        'mobile': int(total_wm * mobile_share)
    }

# Total per category
cat_totals = {}
for cat in ['evaluation', 'feedback', 'research']:
    cat_totals[cat] = sum(cat_current_detail[cat].values())

print("\n=== CURRENT COMPLETED BY CATEGORY ===")
for cat in ['evaluation', 'feedback', 'research']:
    print(f"\n{cat.upper()}: total {cat_totals[cat]}")
    for ch in ['email', 'sms', 'web', 'mobile', 'social']:
        print(f"  {ch}: {cat_current_detail[cat][ch]}")

# Current completed by channel (from channel_performance)
current_per_channel = {'email': 610, 'sms': 552, 'web': 280, 'mobile': 171, 'social': 40}

# Forecast: scale current completed by ratio of new/old budget share
# With constant yield per budget point
print("\n\n=== FORECAST BY CHANNEL ===")
total_forecast = 0
for _, r in channels.iterrows():
    ch = r['channel']
    # Current completed = r['completed_responses']
    # New share = r['final_share']
    # Old share = r['market_share']
    # Forecast = current * (new_share / old_share)
    # But also bounded by capacity (surveys_using_channel)
    factor = r['final_share'] / r['market_share']
    forecast = r['completed_responses'] * factor
    capacity_factor = min(1.5, 1.0 + (r['final_share'] - r['market_share']) / r['market_share'] * 0.5)
    # Apply diminishing returns: if share increases, return per share decreases
    if factor > 1.0:
        # Adjusted: yield_per_point * (1 - 0.3 * log(factor)) for diminishing returns
        adj_yield = r['yield_per_point'] * (1 - 0.2 * np.log(factor))
    else:
        adj_yield = r['yield_per_point']
    forecast_adj = r['final_share'] * 100 * adj_yield
    total_forecast += forecast_adj
    print(f"{ch:>8}: current={int(r['completed_responses'])}, share {r['market_share']:.0%}→{r['final_share']:.1%}, "
          f"forecast={forecast_adj:.1f} (adj yield={adj_yield:.2f})")

print(f"\nTotal forecast (with diminishing returns): {total_forecast:.1f}")
print(f"Current total: {channels['completed_responses'].sum()}")
uplift = (total_forecast - channels['completed_responses'].sum()) / channels['completed_responses'].sum() * 100
print(f"Net uplift: {uplift:+.1f}%")

# Detailed forecast table
print("\n\n=== DETAILED FORECAST TABLE ===")
print(f"{'Channel':<10} {'Current Share':<15} {'Optimal Share':<15} {'Δ Share':<10} {'Current Completed':<20} {'Forecast':<12} {'Change':<10}")
print("="*92)
for _, r in channels.iterrows():
    factor = r['final_share'] / r['market_share']
    delta = (r['final_share'] - r['market_share']) * 100
    if factor > 1.0:
        adj_yield = r['yield_per_point'] * (1 - 0.2 * np.log(factor))
    else:
        adj_yield = r['yield_per_point']
    forecast = r['final_share'] * 100 * adj_yield
    change = forecast - r['completed_responses']
    print(f"{r['channel']:<10} {r['market_share']:<15.1%} {r['final_share']:<15.1%} {delta:+.1f}%{'':<4} {int(r['completed_responses']):<20} {forecast:<12.1f} {change:+.1f}")

print(f"\n{'TOTAL':<10} {'100%':<15} {'100%':<15} {'—':<10} {int(channels['completed_responses'].sum()):<20} {total_forecast:<12.1f} {total_forecast - channels['completed_responses'].sum():+.1f}")

# --- Final comprehensive figures ---

# Fig 8: The complete dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Channel performance scatter
ax = axes[0, 0]
for i, row in channels.iterrows():
    size = row['market_share'] * 1500
    ax.scatter(row['completion_rate'], row['efficiency_score'], s=size, alpha=0.7, edgecolors='black', linewidth=1.5)
    ax.annotate(row['channel'].upper(), (row['completion_rate'], row['efficiency_score']),
                textcoords='offset points', xytext=(5, 5), fontsize=9, fontweight='bold')
ax.set_xlabel('Completion Rate')
ax.set_ylabel('Efficiency Score')
ax.set_title('Channel Performance\n(Bubble = Market Share)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)

# 2. Budget reallocation
ax = axes[0, 1]
x = np.arange(5)
width = 0.35
ax.bar(x - width/2, channels['market_share']*100, width, label='Current', color='#A0A0A0', edgecolor='black')
ax.bar(x + width/2, channels['final_share']*100, width, label='Optimal', color='#2E86AB', edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=9)
ax.set_ylabel('Share (%)')
ax.set_title('Budget Reallocation Plan', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 3. Forecast vs current
ax = axes[0, 2]
baseline = channels['completed_responses'].values
forecast_vals = [channels['final_share'].iloc[i] * 100 * channels['yield_per_point'].iloc[i] for i in range(5)]
ax.bar(x - width/2, baseline, width, label='Current', color='#A0A0A0', edgecolor='black')
ax.bar(x + width/2, forecast_vals, width, label='Forecast', color='#2E86AB', edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=9)
ax.set_ylabel('Completed')
ax.set_title(f'Expected Returns\n(Uplift: {uplift:+.1f}%)', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 4. User lifecycle value cohorts
ax = axes[1, 0]
cohorts = pd.DataFrame({
    'quartile': ['Q1 (Bottom)', 'Q2', 'Q3', 'Q4 (Top)'],
    'share': [0.0, 0.46, 18.32, 81.21]
})
colors_cohort = ['#D3D3D3', '#A9A9A9', '#696969', '#2E86AB']
bars = ax.barh(cohorts['quartile'], cohorts['share'], color=colors_cohort, edgecolor='black')
for bar, val in zip(bars, cohorts['share']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
ax.set_xlabel('% of Total Lifecycle Value')
ax.set_title('User Lifecycle Value Distribution\n(All Users by Quartile)', fontsize=12, fontweight='bold')
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3)

# 5. Category completion by channel (heatmap)
ax = axes[1, 1]
cat_data = []
for ch in ['email', 'sms', 'web', 'mobile', 'social']:
    for cat in ['evaluation', 'feedback', 'research']:
        cat_data.append({'channel': ch.upper(), 'category': cat, 'completion': cat_comp[ch][cat]})
cat_df = pd.DataFrame(cat_data)
pivot = cat_df.pivot(index='channel', columns='category', values='completion')
im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=0.7)
ax.set_xticks(range(3))
ax.set_xticklabels(['Evaluation', 'Feedback', 'Research'], fontsize=9)
ax.set_yticks(range(5))
ax.set_yticklabels(['EMAIL', 'SMS', 'WEB', 'MOBILE', 'SOCIAL'], fontsize=9)
for i in range(5):
    for j in range(3):
        ax.text(j, i, f'{pivot.values[i,j]:.0%}', ha='center', va='center', fontsize=8, fontweight='bold', 
                color='white' if pivot.values[i,j] > 0.35 else 'black')
ax.set_title('Completion Rate by\nChannel × Category', fontsize=12, fontweight='bold')

# 6. Contact-level engagement funnel
ax = axes[1, 2]
funnel_data = pd.DataFrame({
    'metric': ['Open Rate', 'Start Rate', 'Complete Rate'],
    'Email': [0.646, 0.366, 0.116],
    'SMS': [0.667, 0.432, 0.152]
})
x = np.arange(3)
width = 0.35
ax.bar(x - width/2, funnel_data['Email'], width, label='Email', color='#2E86AB', edgecolor='black')
ax.bar(x + width/2, funnel_data['SMS'], width, label='SMS', color='#A23B72', edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(funnel_data['metric'], fontsize=9)
ax.set_ylabel('Rate')
ax.set_title('Contact-Level Engagement\nFunnel (Email vs SMS)', fontsize=12, fontweight='bold')
ax.set_ylim(0, 0.8)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig8_dashboard.png', dpi=150)
plt.close()

print("\n\nDashboard saved as fig8_dashboard.png")

# Compute key metrics for report
print("\n\n=== KEY METRICS FOR REPORT ===")
print(f"Total contacts: 4,000")
print(f"Total lifecycle completed surveys: 14,076")
print(f"Avg lifecycle completed per user: 3.52")
print(f"Multi-channel users (email+SMS): 3,309 (82.7%)")
print(f"  - These users contribute 99.4% of total lifecycle value")
print(f"Email completion rate (channel_performance): 50.5%")
print(f"SMS completion rate: 52.3%")
print(f"Web completion rate: 41.3%")
print(f"Mobile completion rate: 31.6%")
print(f"Social completion rate: 43.7%")
print(f"Email efficiency score: 73.0 (rank 1)")
print(f"SMS efficiency score: 60.1 (rank 3)")
print(f"Web efficiency score: 63.7 (rank 2)")
print(f"Mobile efficiency score: 46.6 (rank 4)")
print(f"Social efficiency score: 41.9 (rank 5)")
print(f"Email category mix: 7.9% eval, 31.4% feedback, 60.7% research")
print(f"SMS category mix: 52.8% eval, 15.3% feedback, 31.9% research")
print(f"Web/Mobile category mix: 19.6% eval, 50.8% feedback, 29.6% research")
print(f"Social category mix: 50.7% eval, 11.9% feedback, 37.4% research")