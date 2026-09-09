import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Core data
channels = pd.DataFrame({
    'channel': ['email', 'sms', 'web', 'mobile', 'social'],
    'surveys_using_channel': [734, 648, 484, 431, 57],
    'total_responses': [1207, 1058, 679, 544, 92],
    'completed_responses': [610, 552, 280, 171, 40],
    'unique_participants': [1025, 899, 577, 462, 78],
    'completion_rate': [0.505, 0.523, 0.413, 0.316, 0.437],
    'efficiency_score': [72.99, 60.11, 63.68, 46.58, 41.94],
    'market_share': [0.35, 0.25, 0.22, 0.18, 0.08],
    'channel_tier': ['Premium', 'Premium', 'Standard', 'Standard', 'Experimental'],
    'strategic_recommendation': ['Optimize', 'Monitor', 'Monitor', 'Review', 'Review']
})

user_value = {'email': 1.0405, 'sms': 1.1718, 'web': 0.978, 'mobile': 0.610, 'social': 1.111}
channels['user_value_factor'] = channels['channel'].map(user_value)
robustness = {'email': 0.959, 'sms': 0.912, 'web': 0.962, 'mobile': 0.962, 'social': 0.089}
channels['category_robustness'] = channels['channel'].map(robustness)

def normalize(s):
    mn, mx = s.min(), s.max()
    return (s - mn) / (mx - mn) if mx > mn else pd.Series([0.5]*len(s))

# Yield per budget point
channels['yield_per_point'] = channels['completed_responses'] / (channels['market_share'] * 100)
channels['n_yield'] = normalize(channels['yield_per_point'])

# Scenario analysis: different weight configurations
scenarios = {
    'Balanced (eff/comp/user/robust)': [0.30, 0.25, 0.25, 0.20],
    'Efficiency-weighted': [0.45, 0.20, 0.20, 0.15],
    'User-value-weighted': [0.20, 0.20, 0.40, 0.20],
    'Completion-weighted': [0.20, 0.40, 0.20, 0.20],
    'ROI-pure (yield only)': None,
}

def allocate_with_floor(score, floors):
    alloc = score / score.sum()
    for _ in range(20):
        for i in range(len(alloc)):
            if alloc[i] < floors[i]:
                alloc[i] = floors[i]
        alloc = alloc / alloc.sum()
    return alloc

floors = {'email': 0.0, 'sms': 0.0, 'web': 0.05, 'mobile': 0.05, 'social': 0.03}
floors_arr = np.array([floors[c] for c in channels['channel']])

results = {}
for name, w in scenarios.items():
    if name == 'ROI-pure (yield only)':
        score = channels['n_yield'] + 0.0001
    else:
        n_eff = normalize(channels['efficiency_score'])
        n_comp = normalize(channels['completion_rate'])
        n_user = normalize(channels['user_value_factor'])
        n_rob = normalize(channels['category_robustness'])
        score = (w[0]*n_eff + w[1]*n_comp + w[2]*n_user + w[3]*n_rob)
        # Blend with yield to avoid myopic allocation
        score = score**0.4 * (channels['n_yield'] + 0.0001)**0.6
    alloc = allocate_with_floor(score, floors_arr)
    forecast = alloc * 100 * channels['yield_per_point']
    results[name] = {
        'alloc': alloc,
        'forecast': forecast,
        'total_forecast': forecast.sum(),
        'uplift': (forecast.sum() - channels['completed_responses'].sum()) / channels['completed_responses'].sum() * 100
    }

# Print scenario table
print("=== SCENARIO ANALYSIS: OPTIMAL ALLOCATION ===")
print(f"{'Scenario':<30} {'email':<8} {'sms':<8} {'web':<8} {'mobile':<8} {'social':<8} {'Forecast':<10} {'Uplift':<8}")
print("="*100)
for name, r in results.items():
    alloc_pct = r['alloc'] * 100
    print(f"{name:<30} {alloc_pct[0]:<8.1f} {alloc_pct[1]:<8.1f} {alloc_pct[2]:<8.1f} {alloc_pct[3]:<8.1f} {alloc_pct[4]:<8.1f} {r['total_forecast']:<10.1f} {r['uplift']:+.1f}%")

# Average allocation across scenarios (robust recommendation)
avg_alloc = np.mean([r['alloc'] for r in results.values()], axis=0)
avg_alloc = avg_alloc / avg_alloc.sum()
avg_forecast = avg_alloc * 100 * channels['yield_per_point']
avg_uplift = (avg_forecast.sum() - channels['completed_responses'].sum()) / channels['completed_responses'].sum() * 100

print(f"\n{'AVERAGE (ROBUST)':<30} {avg_alloc[0]*100:<8.1f} {avg_alloc[1]*100:<8.1f} {avg_alloc[2]*100:<8.1f} {avg_alloc[3]*100:<8.1f} {avg_alloc[4]*100:<8.1f} {avg_forecast.sum():<10.1f} {avg_uplift:+.1f}%")

# Store final recommended allocation
channels['final_share'] = avg_alloc
channels['final_forecast'] = avg_forecast

# Current values
current = channels['completed_responses'].sum()

print("\n\n=== FINAL RECOMMENDED ALLOCATION ===")
print(channels[['channel', 'channel_tier', 'market_share', 'final_share', 'completed_responses', 'final_forecast', 'yield_per_point']].to_string(index=False))
print(f"\nCurrent total completed: {current}")
print(f"Forecast total completed: {avg_forecast.sum():.1f}")
print(f"Net change in completed: {avg_forecast.sum() - current:+.1f} ({avg_uplift:+.1f}%)")

# Save channels for further use
channels.to_csv('/work/channel_model.csv', index=False)

# Sensitivity figure
fig, ax = plt.subplots(figsize=(14, 7))
scen_names = list(results.keys()) + ['Average']
x = np.arange(5)
bar_width = 0.12
colors = ['#2E86AB', '#A23B72', '#F18F01', '#6A994E', '#C73E1D', '#333333']
for i, (name, r) in enumerate(results.items()):
    alloc = r['alloc'] * 100
    ax.bar(x + (i - 2.5) * bar_width, alloc, width=bar_width, label=name, color=colors[i % len(colors)], alpha=0.85, edgecolor='black', linewidth=0.5)
ax.bar(x + 2.5 * bar_width, avg_alloc * 100, width=bar_width, label='Average (Robust)', color='#1B4965', edgecolor='black', linewidth=1.2)
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11, fontweight='bold')
ax.set_ylabel('Optimal Investment Share (%)', fontsize=12)
ax.set_title('Sensitivity Analysis: Optimal Budget Allocation Across Model Scenarios', fontsize=14, fontweight='bold')
ax.legend(fontsize=8, loc='upper center', ncol=3)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig7_sensitivity_allocation.png', dpi=150)
plt.close()

print("\nSaved sensitivity figure.")