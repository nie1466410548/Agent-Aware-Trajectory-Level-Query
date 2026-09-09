import pandas as pd, numpy as np
from scipy.stats import mannwhitneyu

prof = pd.read_csv('/work/user_scored.csv')

# ---- Geographic region mapping ----
def lat_lon_to_region(lat, lon):
    if pd.isna(lat) or pd.isna(lon):
        return 'Unknown'
    if lat >= 15 and lon <= -50:
        return 'North America'
    if lat < 15 and lat >= -60 and lon <= -30:
        return 'South America'
    if lat >= 36 and lon >= -25 and lon <= 45:
        return 'Europe'
    if lat >= 0 and lat < 36 and lon >= -20 and lon <= 52:
        return 'Africa/Middle East'
    if lat >= 0 and lon >= 45 and lon <= 180:
        return 'Asia'
    if lat < 0 and lat >= -50 and lon >= 110:
        return 'Oceania'
    if lat >= 36 and lon >= 45 and lon <= 180:
        return 'Asia'
    if lat >= 0:
        return 'Northern Hemisphere'
    else:
        return 'Southern Hemisphere'

prof['region'] = [lat_lon_to_region(r['avg_lat'], r['avg_lon']) for _, r in prof.iterrows()]
print("Region distribution:")
print(prof.region.value_counts())

# Also create a cleaner continent grouping
continents = ['South America', 'North America', 'Europe', 'Asia', 'Africa/Middle East', 'Oceania']
prof['continent'] = prof['region'].apply(lambda r: r if r in continents else 'Other')

# ---- Medium→High transition analysis ----
med = prof[prof.tier == 'medium_value'].copy()
high = prof[prof.tier == 'high_value'].copy()

print(f"\nMedium: {len(med)}, High: {len(high)}")

dimensions = ['n_survey_responses', 'n_completed', 'completion_rate', 
              'n_channels', 'avg_progress', 'avg_duration', 'active_months',
              'n_active_days', 'n_distinct_surveys']

results = []
for d in dimensions:
    m_m = med[d].mean()
    h_m = high[d].mean()
    stat, p = mannwhitneyu(high[d], med[d], alternative='two-sided')
    pooled_std = np.sqrt((med[d].std()**2 + high[d].std()**2) / 2)
    cohens_d = (h_m - m_m) / pooled_std if pooled_std > 0 else 0
    results.append({
        'dimension': d,
        'medium_mean': round(m_m, 3),
        'high_mean': round(h_m, 3),
        'diff': round(h_m - m_m, 3),
        'pct_improvement': round((h_m - m_m) / m_m * 100, 1) if m_m > 0 else None,
        'p_value': round(p, 6),
        'cohens_d': round(cohens_d, 3)
    })

res_df = pd.DataFrame(results).sort_values('cohens_d', ascending=False)
print("\nMedium → High transition drivers (sorted by effect size):")
print(res_df.to_string(index=False))

prof.to_csv('/work/user_scored.csv', index=False)