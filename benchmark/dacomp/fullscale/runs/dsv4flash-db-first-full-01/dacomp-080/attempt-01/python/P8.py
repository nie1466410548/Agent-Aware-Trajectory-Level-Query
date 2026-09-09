import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

prof = pd.read_csv('/work/user_scored.csv')

# Fix region mapping - use proper continent boundaries
def lat_lon_to_continent(lat, lon):
    if pd.isna(lat) or pd.isna(lon):
        return 'Other'
    # North America
    if 25 <= lat <= 72 and -170 <= lon <= -50:
        return 'North America'
    # South America
    if -60 <= lat <= -5 and -90 <= lon <= -30:
        return 'South America'
    # Europe (rough)
    if 36 <= lat <= 70 and -25 <= lon <= 45:
        return 'Europe'
    # Africa
    if -35 <= lat <= 37 and -20 <= lon <= 52:
        return 'Africa'
    # Asia
    if 0 <= lat <= 75 and 45 <= lon <= 180:
        return 'Asia'
    # Oceania
    if -50 <= lat <= -10 and 110 <= lon <= 180:
        return 'Oceania'
    # Central America / Caribbean
    if 5 <= lat < 25 and -120 <= lon <= -50:
        return 'Central America'
    return 'Other'

prof['continent2'] = [lat_lon_to_continent(r['avg_lat'], r['avg_lon']) for _, r in prof.iterrows()]

# Combine Central America with North America
prof['continent'] = prof['continent2'].replace({'Central America': 'North America'})
print("Continent distribution:")
print(prof.continent.value_counts())

# Recalculate region aggregates
region_agg = prof.groupby('continent').agg(
    n_users=('email','count'),
    avg_score=('value_score','mean'),
    avg_freq=('n_survey_responses','mean'),
    avg_completion=('completion_rate','mean'),
    avg_channels=('n_channels','mean'),
    pct_high_power=('tier', lambda s: 100*(s.isin(['high_value','power_user'])).mean()),
    pct_power=('tier', lambda s: 100*(s=='power_user').mean()),
    pct_one_time=('tier', lambda s: 100*(s=='one_time').mean())
).sort_values('avg_score', ascending=False)
print("\n=== Value by continent ===")
print(region_agg.round(1).to_string())

# Crosstab
ct_reg = pd.crosstab(prof.continent, prof.tier, normalize='index')*100
print("\n=== Tier composition by continent (row %) ===")
print(ct_reg.round(1).to_string())

prof.to_csv('/work/user_scored.csv', index=False)

# ---- Visualizations ----
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# 1. Score distribution histogram
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(prof.value_score, bins=30, kde=True, color='steelblue', ax=ax)
for t, color in [('one_time', '#95a5a6'), ('low_value', '#e74c3c'), 
                  ('medium_value', '#f39c12'), ('high_value', '#3498db'),
                  ('power_user', '#2ecc71')]:
    med = prof[prof.tier==t].value_score.median()
    ax.axvline(med, color=color, ls='--', lw=1, alpha=0.7)
ax.set_xlabel('Value Score (0-100)', fontsize=12)
ax.set_ylabel('Number of Users', fontsize=12)
ax.set_title('User Value Score Distribution with Tier Medians', fontsize=14)
ax.legend(['one_time (median)', 'low_value (median)', 'medium_value (median)', 
           'high_value (median)', 'power_user (median)'])
plt.tight_layout()
plt.savefig('/work/fig1_score_distribution.png', dpi=120)
plt.close()
print("Saved fig1_score_distribution.png")

# 2. Tier composition and value contribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

tier_order = ['one_time', 'low_value', 'medium_value', 'high_value', 'power_user']
colors = ['#95a5a6', '#e74c3c', '#f39c12', '#3498db', '#2ecc71']

# Population share
pop_share = prof.tier.value_counts()[tier_order].values
ax1.bar(tier_order, pop_share, color=colors)
ax1.set_title('User Count by Tier', fontsize=13)
ax1.set_ylabel('Number of Users')
for i, v in enumerate(pop_share):
    ax1.text(i, v+20, f'{v/len(prof)*100:.1f}%', ha='center', fontweight='bold')

# Response contribution share
resp_share = [prof[prof.tier==t].n_survey_responses.sum() for t in tier_order]
ax2.bar(tier_order, resp_share, color=colors)
ax2.set_title('Total Survey Responses by Tier', fontsize=13)
ax2.set_ylabel('Number of Responses')
for i, v in enumerate(resp_share):
    ax2.text(i, v+30, f'{v/prof.n_survey_responses.sum()*100:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/fig2_tier_contribution.png', dpi=120)
plt.close()
print("Saved fig2_tier_contribution.png")

# 3. Medium vs High comparison radar/dot chart
fig, ax = plt.subplots(figsize=(12, 6))
dims = ['n_survey_responses', 'completion_rate', 'n_channels', 'active_months', 'avg_progress']
med = prof[prof.tier=='medium_value']
high = prof[prof.tier=='high_value']

x = np.arange(len(dims))
w = 0.35
med_vals = [med[d].mean() for d in dims]
high_vals = [high[d].mean() for d in dims]
ax.bar(x - w/2, med_vals, w, label='Medium Value', color='#f39c12', alpha=0.8)
ax.bar(x + w/2, high_vals, w, label='High Value', color='#3498db', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(['Survey Responses', 'Completion Rate', 'Channels Used', 'Active Months', 'Avg Progress'], fontsize=11)
ax.set_ylabel('Mean Value', fontsize=12)
ax.set_title('Behavioral Profile Comparison: Medium vs High Value Users', fontsize=14)
ax.legend(fontsize=12)
# Annotate % improvements
for i, (mv, hv) in enumerate(zip(med_vals, high_vals)):
    pct = (hv - mv) / mv * 100
    ax.annotate(f'+{pct:.0f}%', (i + w/2, hv), textcoords="offset points", xytext=(0, 5),
                ha='center', fontsize=9, fontweight='bold', color='#3498db')
plt.tight_layout()
plt.savefig('/work/fig3_medium_vs_high.png', dpi=120)
plt.close()
print("Saved fig3_medium_vs_high.png")

# 4. Average score by language and continent
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

lang_order = prof.groupby('dom_lang')['value_score'].mean().sort_values(ascending=False).index
sns.barplot(x='dom_lang', y='value_score', data=prof, order=lang_order, 
            palette='Blues_d', ax=ax1)
ax1.set_title('Average Value Score by Language', fontsize=13)
ax1.set_xlabel('Language')
ax1.set_ylabel('Avg Value Score')

cont_order = prof.groupby('continent')['value_score'].mean().sort_values(ascending=False).index
sns.barplot(x='continent', y='value_score', data=prof, order=cont_order,
            palette='Greens_d', ax=ax2)
ax2.set_title('Average Value Score by Continent', fontsize=13)
ax2.set_xlabel('Continent')
ax2.set_ylabel('Avg Value Score')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=15)

plt.tight_layout()
plt.savefig('/work/fig4_lang_region_scores.png', dpi=120)
plt.close()
print("Saved fig4_lang_region_scores.png")

# 5. Heatmap of tier composition by language/continent
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

# Language x tier heatmap
ct_lang = pd.crosstab(prof.dom_lang, prof.tier, normalize='index')
ct_lang = ct_lang[tier_order]
sns.heatmap(ct_lang, annot=True, fmt='.1%', cmap='YlOrRd', ax=ax1, cbar_kws={'label': 'Proportion'})
ax1.set_title('Tier Composition by Language', fontsize=13)
ax1.set_xlabel('Tier')
ax1.set_ylabel('Language')

# Continent x tier heatmap
ct_cont = pd.crosstab(prof.continent, prof.tier, normalize='index')
ct_cont = ct_cont[tier_order]
sns.heatmap(ct_cont, annot=True, fmt='.1%', cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'Proportion'})
ax2.set_title('Tier Composition by Continent', fontsize=13)
ax2.set_xlabel('Tier')
ax2.set_ylabel('Continent')

plt.tight_layout()
plt.savefig('/work/fig5_tier_heatmap.png', dpi=120)
plt.close()
print("Saved fig5_tier_heatmap.png")

# 6. Score component breakdown by tier
fig, ax = plt.subplots(figsize=(12, 6))
components = ['freq_score', 'completion_score', 'channel_score', 'progress_score']
comp_labels = ['Participation\nFrequency', 'Completion\nRate', 'Cross-Channel\nActivity', 'Engagement\nDepth']
comp_colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']

tier_scores = prof.groupby('tier')[components].mean().loc[tier_order]
bottom = np.zeros(len(tier_order))
for i, (comp, label, color) in enumerate(zip(components, comp_labels, comp_colors)):
    vals = tier_scores[comp].values
    ax.bar(tier_order, vals, bottom=bottom, label=label, color=color, alpha=0.85)
    bottom += vals

ax.set_ylabel('Score Contribution', fontsize=12)
ax.set_title('Value Score Decomposition by Tier', fontsize=14)
ax.legend(fontsize=11)
for i, t in enumerate(tier_order):
    ax.text(i, bottom[i] + 1, f'{bottom[i]:.0f}', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('/work/fig6_score_decomposition.png', dpi=120)
plt.close()
print("Saved fig6_score_decomposition.png")