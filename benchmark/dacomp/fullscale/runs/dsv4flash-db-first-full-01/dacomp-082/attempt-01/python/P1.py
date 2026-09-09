import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import json, os, math

# ──────────────────────────────────────────────────────────
# 1. CHANNEL PERFORMANCE DATA (from table)
# ──────────────────────────────────────────────────────────
channels = pd.DataFrame({
    'channel': ['email', 'sms', 'web', 'mobile', 'social'],
    'surveys_using_channel': [734, 648, 484, 431, 57],
    'total_responses': [1207, 1058, 679, 544, 92],
    'completed_responses': [610, 552, 280, 171, 40],
    'unique_participants': [1025, 899, 577, 462, 78],
    'completion_rate': [0.5054475483, 0.5225522529, 0.4129312607, 0.3155053704, 0.4366380843],
    'avg_progress': [52.22536136, 49.0954496, 43.0588963, 26.86089276, 48.92087824],
    'avg_duration': [1465.907225, 1941.887858, 2077.430159, 1855.356179, 1763.669483],
    'efficiency_score': [72.98788342, 60.10784008, 63.68488643, 46.5811312, 41.9384134],
    'market_share': [0.35, 0.25, 0.22, 0.18, 0.08],
    'completion_rank': [2, 1, 4, 5, 3],
    'efficiency_rank': [1, 3, 2, 4, 5],
    'channel_tier': ['Tier 1 - Premium', 'Tier 1 - Premium', 'Tier 2 - Standard', 'Tier 2 - Standard', 'Tier 3 - Experimental'],
    'strategic_recommendation': ['Optimize', 'Monitor', 'Monitor', 'Review', 'Review']
})

# ──────────────────────────────────────────────────────────
# 2. SURVEY TABLE: Channel × Project Category Completion
# ──────────────────────────────────────────────────────────
# Per-channel response counts by category (from survey table)
cat_data = {
    ('email', 'evaluation'): (4913, 2840),
    ('email', 'feedback'): (19565, 11870),
    ('email', 'research'): (37849, 24183),
    ('sms', 'evaluation'): (13192, 6949),
    ('sms', 'feedback'): (3829, 1627),
    ('sms', 'research'): (7949, 3899),
    ('social', 'evaluation'): (1788, 298),
    ('social', 'feedback'): (420, 5),
    ('social', 'research'): (1322, 56),
    ('web_mobile', 'evaluation'): (15814, 6485),
    ('web_mobile', 'feedback'): (41054, 15559),
    ('web_mobile', 'research'): (23965, 9052)
}

cat_rows = []
for (ch, cat), (r, c) in cat_data.items():
    cat_rows.append({'channel': ch, 'category': cat, 'responses': r, 'completed': c, 'completion': c/r if r>0 else 0})
cat_df = pd.DataFrame(cat_rows)

# ──────────────────────────────────────────────────────────
# 3. CONTACT TABLE: User Lifecycle Value
# ──────────────────────────────────────────────────────────
# Overall stats
overall_avg_ltv = 3.519
total_contacts = 4000
total_completed_all = 14076

# Email users (sent_email > 0): avg LTV
email_users_avg_ltv = 3.6615
sms_users_avg_ltv = 4.1234
# Email-only users
email_only_avg_ltv = 0.1447
sms_only_avg_ltv = 0.1395
both_avg_ltv = 4.2269

# Cohort quartile distribution (all users)
cohorts_all = pd.DataFrame({
    'quartile': [1, 2, 3, 4],
    'users': [1000, 1000, 1000, 1000],
    'total_ltv': [0, 65, 2579, 11432],
    'avg_ltv': [0.0, 0.065, 2.579, 11.432],
    'share_pct': [0.0, 0.46, 18.32, 81.21]
})

# Email users cohort
email_cohorts = pd.DataFrame({
    'quartile': [1, 2, 3, 4],
    'users': [961, 960, 960, 960],
    'total_ltv': [0, 139, 2693, 11232],
    'avg_ltv': [0.0, 0.145, 2.805, 11.7],
    'share_pct': [0.0, 0.99, 19.14, 79.87]
})

# SMS users cohort
sms_cohorts = pd.DataFrame({
    'quartile': [1, 2, 3, 4],
    'users': [849, 849, 849, 848],
    'total_ltv': [0, 420, 2922, 10657],
    'avg_ltv': [0.0, 0.495, 3.442, 12.567],
    'share_pct': [0.0, 2.99, 20.87, 76.14]
})

# Per-channel engagement funnel (from contact)
contact_funnel = pd.DataFrame({
    'metric': ['open_rate', 'start_rate', 'complete_rate'],
    'email': [0.646, 0.366, 0.116],
    'sms': [0.667, 0.432, 0.152]
})

# ──────────────────────────────────────────────────────────
# 4. COMPOSITE ROI MODEL
# ──────────────────────────────────────────────────────────
# Normalize function (min-max)
def normalize(s):
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series([0.5]*len(s))
    return (s - mn) / (mx - mn)

# Per-channel user value factor
# Email & sms: from contact LTV; web/mobile/social: from avg_progress
user_value = {
    'email': email_users_avg_ltv / overall_avg_ltv,  # 1.040
    'sms': sms_users_avg_ltv / overall_avg_ltv,       # 1.172
    'web': 0.978,  # avg_progress 43.06 / 44.04
    'mobile': 0.610,  # avg_progress 26.86 / 44.04
    'social': 1.111  # avg_progress 48.92 / 44.04
}
channels['user_value_factor'] = channels['channel'].map(user_value)

# Category robustness: 1 - CV of completion rates across categories
# email: 0.578, 0.607, 0.639
# sms: 0.527, 0.425, 0.491
# social: 0.167, 0.012, 0.042
# web_mobile (for web & mobile): 0.410, 0.379, 0.378
cat_comp = {
    'email': [0.578, 0.607, 0.639],
    'sms': [0.527, 0.425, 0.491],
    'social': [0.167, 0.012, 0.042],
    'web_mobile': [0.410, 0.379, 0.378]
}
robustness = {}
for ch, rates in cat_comp.items():
    mu = np.mean(rates)
    cv = np.std(rates) / mu if mu > 0 else 1.0
    robustness[ch] = max(0, 1 - cv)
# Assign web and mobile same as web_mobile
robustness['web'] = robustness['web_mobile']
robustness['mobile'] = robustness['web_mobile']
channels['category_robustness'] = channels['channel'].map(robustness)

# Normalize metrics
channels['n_eff'] = normalize(channels['efficiency_score'])
channels['n_comp'] = normalize(channels['completion_rate'])
channels['n_user'] = normalize(channels['user_value_factor'])
channels['n_robust'] = normalize(channels['category_robustness'])

# Composite Effectiveness Score (CES) - weighted sum
weights = {'eff': 0.35, 'comp': 0.25, 'user': 0.25, 'robust': 0.15}
channels['CES'] = (weights['eff'] * channels['n_eff'] +
                   weights['comp'] * channels['n_comp'] +
                   weights['user'] * channels['n_user'] +
                   weights['robust'] * channels['n_robust'])

# Current budget share (market share)
channels['current_share'] = channels['market_share']

# Optimal investment ratio (proportional to CES, with floor for experimental)
raw_optimal = channels['CES'] / channels['CES'].sum()
# Apply floor: 5% minimum for social (experimental), recalc
MIN_FLOOR = 0.03  # 3% minimum for experimental
# Consider tiers: Tier 3 gets floor, Tier 2 gets 5% min, Tier 1 unlimited
tier_min = {'Tier 1 - Premium': 0.0, 'Tier 2 - Standard': 0.05, 'Tier 3 - Experimental': MIN_FLOOR}
channels['min_floor'] = channels['channel_tier'].map(tier_min)

# Iterative allocation with floor constraint
optimal = raw_optimal.copy()
# First pass: allocate floor
total_floor = sum(max(0, tier_min[t] - optimal[i]) if optimal[i] < tier_min[t] else 0 
                  for i, t in enumerate(channels['channel_tier']))
# Actually simpler: clip to floor, then renormalize
for i in range(5):
    if optimal[i] < channels['min_floor'].iloc[i]:
        optimal[i] = channels['min_floor'].iloc[i]
# Normalize to sum to 1
channels['optimal_share'] = optimal / optimal.sum()

# ROI: value per unit of budget share
# Value = completed_responses × user_value_factor
channels['value_output'] = channels['completed_responses'] * channels['user_value_factor']
# Current ROI = value / current_share
channels['current_ROI'] = channels['value_output'] / channels['current_share']
# Optimal ROI = value / optimal_share
channels['optimal_ROI'] = channels['value_output'] / channels['optimal_share']

# Yield per budget point (completions per 1% share)
channels['yield_per_point'] = channels['completed_responses'] / (channels['current_share'] * 100)

# Forecast: Apply optimal shares to yield
total_budget = 1.0  # 100%
total_completed_current = channels['completed_responses'].sum()
channels['forecast_completed'] = channels['optimal_share'] * 100 * channels['yield_per_point']
total_forecast = channels['forecast_completed'].sum()

# Expected return uplift
uplift = (total_forecast - total_completed_current) / total_completed_current * 100

print("=== CHANNEL PERFORMANCE & ROI MODEL ===")
print(channels[['channel', 'channel_tier', 'completion_rate', 'efficiency_score', 
                'user_value_factor', 'category_robustness', 'CES',
                'current_share', 'optimal_share', 'current_ROI', 'yield_per_point',
                'forecast_completed']].to_string(index=False))
print(f"\nTotal completed (current): {total_completed_current}")
print(f"Total completed (forecast): {total_forecast:.1f}")
print(f"Expected uplift: {uplift:.1f}%")

# ──────────────────────────────────────────────────────────
# 5. VISUALIZATIONS
# ──────────────────────────────────────────────────────────
os.makedirs('/work', exist_ok=True)

# ---- Fig 1: Completion vs Efficiency scatter ----
fig, ax = plt.subplots(figsize=(10, 6))
colors = {'email': '#2E86AB', 'sms': '#A23B72', 'web': '#F18F01', 'mobile': '#C73E1D', 'social': '#6A994E'}
sizes = channels['market_share'] * 1200
for i, row in channels.iterrows():
    ax.scatter(row['completion_rate'], row['efficiency_score'], 
               s=sizes.iloc[i], c=colors[row['channel']], alpha=0.7, edgecolors='black', linewidth=1.5,
               label=f"{row['channel']} (share={row['market_share']:.0%})")
    ax.annotate(row['channel'].upper(), (row['completion_rate'], row['efficiency_score']),
                xytext=(5, 5), textcoords='offset points', fontsize=11, fontweight='bold')
ax.set_xlabel('Completion Rate', fontsize=12)
ax.set_ylabel('Efficiency Score', fontsize=12)
ax.set_title('Channel Performance: Completion vs Efficiency\n(Bubble size = Market Share)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='lower left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig1_channel_performance_scatter.png', dpi=150)
plt.close()

# ---- Fig 2: Channel × Category Completion Heatmap ----
fig, ax = plt.subplots(figsize=(10, 6))
heat_data = cat_df.pivot_table(index='channel', columns='category', values='completion')
sns.heatmap(heat_data, annot=True, fmt='.1%', cmap='RdYlGn', ax=ax, 
            linewidths=1, cbar_kws={'label': 'Completion Rate'})
ax.set_title('Channel Completion Rate by Project Category\n(Survey Table)', fontsize=14, fontweight='bold')
ax.set_xlabel('Project Category', fontsize=12)
ax.set_ylabel('Distribution Channel', fontsize=12)
plt.tight_layout()
plt.savefig('/work/fig2_category_completion_heatmap.png', dpi=150)
plt.close()

# ---- Fig 3: Cohort Value Distribution ----
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
cohorts_list = [('All Users', cohorts_all), ('Email Users', email_cohorts), ('SMS Users', sms_cohorts)]
for ax, (title, df) in zip(axes, cohorts_list):
    bars = ax.bar(df['quartile'].astype(str), df['share_pct'], color=['#E0E0E0', '#B0B0B0', '#707070', '#2E86AB'],
                  edgecolor='black', linewidth=1.5)
    for bar, val in zip(bars, df['share_pct']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%', 
                ha='center', fontsize=10, fontweight='bold')
    ax.set_title(f'{title} - LTV Cohorts', fontsize=13, fontweight='bold')
    ax.set_xlabel('Quartile (by Completed Surveys)', fontsize=10)
    ax.set_ylabel('% of Total Lifecycle Value', fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig3_cohort_value_distribution.png', dpi=150)
plt.close()

# ---- Fig 4: Current vs Optimal Investment Ratios ----
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(5)
width = 0.35
bars1 = ax.bar(x - width/2, channels['current_share']*100, width, label='Current Budget Share', color='#A0A0A0', edgecolor='black')
bars2 = ax.bar(x + width/2, channels['optimal_share']*100, width, label='Optimal Investment Ratio', color='#2E86AB', edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11)
ax.set_ylabel('Share of Budget (%)', fontsize=12)
ax.set_title('Channel Budget Reallocation: Current vs Optimal', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.1f}%', 
            ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{bar.get_height():.1f}%', 
            ha='center', fontsize=9, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig4_budget_reallocation.png', dpi=150)
plt.close()

# ---- Fig 5: Forecast of Expected Returns ----
fig, ax = plt.subplots(figsize=(10, 6))
baseline = channels['completed_responses'].values
forecast = channels['forecast_completed'].values
x = np.arange(5)
width = 0.35
bars1 = ax.bar(x - width/2, baseline, width, label='Current Completed', color='#A0A0A0', edgecolor='black')
bars2 = ax.bar(x + width/2, forecast, width, label='Forecast Completed', color='#2E86AB', edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(channels['channel'].str.upper(), fontsize=11)
ax.set_ylabel('Completed Responses', fontsize=12)
ax.set_title(f'Expected Returns: Current vs Forecast\n(Total uplift: {uplift:.1f}%)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{int(bar.get_height())}', 
            ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{int(bar.get_height())}', 
            ha='center', fontsize=9, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig5_forecast_returns.png', dpi=150)
plt.close()

print("\n=== MODEL DETAILS ===")
print(f"Weights: efficiency={weights['eff']}, completion={weights['comp']}, user_value={weights['user']}, robustness={weights['robust']}")
print(f"\nUser Value Factors: {user_value}")
print(f"\nCategory Robustness (1-CV): {robustness}")

# Category-level analysis table
print("\n\n=== CATEGORY-LEVEL CHANNEL COMPLETION ===")
for ch in ['email', 'sms', 'social', 'web_mobile']:
    sub = cat_df[cat_df['channel'] == ch]
    print(f"\n{ch.upper()}:")
    for _, r in sub.iterrows():
        print(f"  {r['category']}: {r['responses']} responses, {r['completed']} completed, {r['completion']:.1%}")

# Channel response mix by category
print("\n\n=== CHANNEL MIX BY CATEGORY (Survey Table) ===")
for ch in ['email', 'sms', 'social', 'web_mobile']:
    sub = cat_df[cat_df['channel'] == ch]
    total = sub['responses'].sum()
    print(f"\n{ch.upper()} (total={total}):")
    for _, r in sub.iterrows():
        pct = r['responses'] / total * 100
        print(f"  {r['category']}: {r['responses']} ({pct:.1f}%)")

# Contact funnel comparison
print("\n\n=== CONTACT-LEVEL ENGAGEMENT FUNNEL ===")
print(contact_funnel.to_string(index=False))