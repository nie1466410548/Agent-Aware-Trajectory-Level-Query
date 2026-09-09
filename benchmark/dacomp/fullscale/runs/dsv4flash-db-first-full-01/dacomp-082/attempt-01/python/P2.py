import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Data
channels = pd.DataFrame({
    'channel': ['email', 'sms', 'web', 'mobile', 'social'],
    'surveys_using_channel': [734, 648, 484, 431, 57],
    'total_responses': [1207, 1058, 679, 544, 92],
    'completed_responses': [610, 552, 280, 171, 40],
    'unique_participants': [1025, 899, 577, 462, 78],
    'completion_rate': [0.505, 0.523, 0.413, 0.316, 0.437],
    'efficiency_score': [72.99, 60.11, 63.68, 46.58, 41.94],
    'market_share': [0.35, 0.25, 0.22, 0.18, 0.08],
    'channel_tier': ['Tier 1 - Premium', 'Tier 1 - Premium', 'Tier 2 - Standard', 'Tier 2 - Standard', 'Tier 3 - Experimental'],
    'strategic_recommendation': ['Optimize', 'Monitor', 'Monitor', 'Review', 'Review']
})

# User value factors
user_value = {'email': 1.0405, 'sms': 1.1718, 'web': 0.978, 'mobile': 0.610, 'social': 1.111}
channels['user_value_factor'] = channels['channel'].map(user_value)

# Category robustness
robustness = {'email': 0.959, 'sms': 0.912, 'web': 0.962, 'mobile': 0.962, 'social': 0.089}
channels['category_robustness'] = channels['channel'].map(robustness)

# Normalize function
def normalize(s):
    mn, mx = s.min(), s.max()
    return (s - mn) / (mx - mn) if mx > mn else pd.Series([0.5]*len(s))

channels['n_eff'] = normalize(channels['efficiency_score'])
channels['n_comp'] = normalize(channels['completion_rate'])
channels['n_user'] = normalize(channels['user_value_factor'])
channels['n_robust'] = normalize(channels['category_robustness'])

# Yield = completed responses per 1% market share
channels['yield_per_point'] = channels['completed_responses'] / (channels['market_share'] * 100)

# Normalize yield
channels['n_yield'] = normalize(channels['yield_per_point'])

# --- REVISED MODEL ---
# Composite score = geometric mean of quality (CES) and efficiency (yield)
# CES uses efficiency, completion, user value, robustness
weights = {'eff': 0.30, 'comp': 0.25, 'user': 0.25, 'robust': 0.20}
channels['CES'] = (weights['eff'] * channels['n_eff'] +
                   weights['comp'] * channels['n_comp'] +
                   weights['user'] * channels['n_user'] +
                   weights['robust'] * channels['n_robust'])

# Combined allocation score = CES^0.4 * n_yield^0.6 
# (more weight on yield since it directly measures returns per budget)
channels['alloc_score'] = (channels['CES'] ** 0.4) * (channels['n_yield'] ** 0.6)

# Apply tier-based minimum floors
tier_min = {'Tier 1 - Premium': 0.0, 'Tier 2 - Standard': 0.05, 'Tier 3 - Experimental': 0.03}
channels['min_floor'] = channels['channel_tier'].map(tier_min)

# Iterative allocation with floor constraints
raw_alloc = channels['alloc_score'] / channels['alloc_score'].sum()
# Apply floors iteratively
alloc = raw_alloc.copy()
for iteration in range(10):
    for i in range(5):
        if alloc[i] < channels['min_floor'].iloc[i]:
            alloc[i] = channels['min_floor'].iloc[i]
    alloc = alloc / alloc.sum()  # renormalize

channels['optimal_share'] = alloc

# Also compute a pure ROI-maximizing allocation (for comparison)
# ROI = completed_responses * user_value_factor / market_share
channels['ROI'] = channels['completed_responses'] * channels['user_value_factor'] / channels['market_share']
roi_alloc = channels['ROI'] / channels['ROI'].sum()
# Apply same floors
roi_alloc_constrained = roi_alloc.copy()
for iteration in range(10):
    for i in range(5):
        if roi_alloc_constrained[i] < channels['min_floor'].iloc[i]:
            roi_alloc_constrained[i] = channels['min_floor'].iloc[i]
    roi_alloc_constrained = roi_alloc_constrained / roi_alloc_constrained.sum()

# Forecast: expected completed = optimal_share * 100 * yield_per_point
total_completed_current = channels['completed_responses'].sum()
channels['forecast_completed'] = channels['optimal_share'] * 100 * channels['yield_per_point']
total_forecast = channels['forecast_completed'].sum()
uplift = (total_forecast - total_completed_current) / total_completed_current * 100

# Comparison tables
print("=== REVISED CHANNEL ROI MODEL ===")
print(f"{'Channel':<10} {'Tier':<25} {'CompRate':<10} {'EffScore':<10} {'UserVal':<10} {'Robust':<10} {'CES':<8} {'Yield':<10} {'AllocScore':<12} {'CurShare':<10} {'OptShare':<10} {'Forecast':<10}")
print("="*140)
for _, r in channels.iterrows():
    print(f"{r['channel']:<10} {r['channel_tier']:<25} {r['completion_rate']:<10.3f} {r['efficiency_score']:<10.2f} {r['user_value_factor']:<10.4f} {r['category_robustness']:<10.3f} {r['CES']:<8.4f} {r['yield_per_point']:<10.2f} {r['alloc_score']:<12.4f} {r['market_share']:<10.2%} {r['optimal_share']:<10.2%} {r['forecast_completed']:<10.1f}")

print(f"\nCurrent total completed: {total_completed_current}")
print(f"Forecast total completed: {total_forecast:.1f}")
print(f"Expected uplift: {uplift:+.1f}%")

# Also show ROI-based allocation
print("\n\n=== COMPARISON: Current vs ROI-Maximizing vs Optimal (Composite) ===")
comp = pd.DataFrame({
    'channel': channels['channel'],
    'current_share': channels['market_share'],
    'roi_share': roi_alloc_constrained.values,
    'optimal_share': channels['optimal_share'].values
})
print(comp.to_string(index=False))

# ROI-maximizing forecast
roi_forecast = roi_alloc_constrained * 100 * channels['yield_per_point']
print(f"\nROI-maximizing total forecast: {roi_forecast.sum():.1f}")
print(f"Composite model total forecast: {total_forecast:.1f}")

# Category-level channel mix (from survey)
print("\n\n=== CATEGORY MIX PER CHANNEL (Survey Table) ===")
cat_mix = {
    'email': {'evaluation': 0.079, 'feedback': 0.314, 'research': 0.607},
    'sms': {'evaluation': 0.528, 'feedback': 0.153, 'research': 0.319},
    'social': {'evaluation': 0.507, 'feedback': 0.119, 'research': 0.374},
    'web_mobile': {'evaluation': 0.196, 'feedback': 0.508, 'research': 0.296}
}
for ch, mix in cat_mix.items():
    print(f"\n{ch.upper()}:")
    for cat, pct in mix.items():
        print(f"  {cat}: {pct:.1%}")

# Category completion rates by channel
cat_comp = {
    'email': {'evaluation': 0.578, 'feedback': 0.607, 'research': 0.639},
    'sms': {'evaluation': 0.527, 'feedback': 0.425, 'research': 0.491},
    'social': {'evaluation': 0.167, 'feedback': 0.012, 'research': 0.042},
    'web_mobile': {'evaluation': 0.410, 'feedback': 0.379, 'research': 0.378}
}
print("\n\n=== COMPLETION RATE BY CHANNEL × CATEGORY ===")
for ch, rates in cat_comp.items():
    print(f"\n{ch.upper()}:")
    for cat, rate in rates.items():
        print(f"  {cat}: {rate:.1%}")

# ---- Revised Visualizations ----
os.makedirs('/work', exist_ok=True)

# Fig 4 revised: Budget reallocation comparison
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(5)
width = 0.25
bars1 = ax.bar(x - width, channels['market_share']*100, width, label='Current Budget Share', color='#A0A0A0', edgecolor='black', alpha=0.8)
bars2 = ax.bar(x, channels['optimal_share']*100, width, label='Optimal (Composite)', color='#2E86AB', edgecolor='black')
bars3 = ax.bar(x + width, roi_alloc_constrained*100, width, label='ROI-Maximizing', color='#A23B72', edgecolor='black', alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11, fontweight='bold')
ax.set_ylabel('Share of Budget (%)', fontsize=12)
ax.set_title('Channel Budget Reallocation: Three Scenarios', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=8, fontweight='bold')
for bar in bars3:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig4_budget_reallocation_v2.png', dpi=150)
plt.close()

# Fig 5: Forecast returns comparison
fig, ax = plt.subplots(figsize=(12, 6))
baseline = channels['completed_responses'].values
forecast_opt = channels['forecast_completed'].values
forecast_roi = roi_forecast.values
x = np.arange(5)
width = 0.25
bars1 = ax.bar(x - width, baseline, width, label='Current Completed', color='#A0A0A0', edgecolor='black', alpha=0.8)
bars2 = ax.bar(x, forecast_opt, width, label=f'Forecast (Composite, +{uplift:.1f}%)', color='#2E86AB', edgecolor='black')
bars3 = ax.bar(x + width, forecast_roi, width, label=f'Forecast (ROI-Max, +{((roi_forecast.sum()-total_completed_current)/total_completed_current*100):.1f}%)', color='#A23B72', edgecolor='black', alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11, fontweight='bold')
ax.set_ylabel('Completed Responses', fontsize=12)
ax.set_title('Expected Returns: Current vs Forecast Under Reallocation', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{int(bar.get_height())}', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{int(bar.get_height())}', ha='center', fontsize=8, fontweight='bold')
for bar in bars3:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{int(bar.get_height())}', ha='center', fontsize=8)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig5_forecast_returns_v2.png', dpi=150)
plt.close()

# Fig 6: Category contribution radar
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
categories = ['evaluation', 'feedback', 'research']
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]
channel_colors = {'email': '#2E86AB', 'sms': '#A23B72', 'web_mobile': '#F18F01', 'social': '#6A994E'}
for ch, label in [('email', 'Email'), ('sms', 'SMS'), ('web_mobile', 'Web/Mobile'), ('social', 'Social')]:
    rates = [cat_comp[ch][c] for c in categories]
    rates += rates[:1]
    ax.plot(angles, rates, 'o-', linewidth=2, label=label, color=channel_colors.get(ch, '#333'))
    ax.fill(angles, rates, alpha=0.1, color=channel_colors.get(ch, '#333'))
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_ylim(0, 0.7)
ax.set_title('Channel Completion Rate by Category\n(Polar Comparison)', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
plt.savefig('/work/fig6_category_radar.png', dpi=150)
plt.close()

print("\n\n=== KEY INSIGHTS SUMMARY ===")
print("1. SMS has the highest yield (22.1 completions per 1% budget share) and highest user value (LTV factor 1.17)")
print("2. Email has the highest efficiency score (73.0) and consistent completion across categories (57-64%)")
print("3. Web/Mobile show moderate performance but dominate feedback surveys (50.8% of web/mobile responses)")
print("4. Social has extremely low completion rates (1-17%) and category robustness is poor")
print("5. Multi-channel users (email + sms) have 4.2x higher lifecycle value than single-channel users")
print("6. Top quartile users contribute 81% of total lifecycle value - retention is critical")