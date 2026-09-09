import pandas as pd
import numpy as np

# Get all relevant data
comp = db.frame(db.query("SELECT company_id, company_name, created_at, all_company_tags FROM intercom__company_enhanced"))
metrics = db.frame(db.query("SELECT * FROM intercom__company_metrics"))

# Parse tags
def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['company_id'] = comp['company_id']
parsed['company_name'] = comp['company_name']
parsed['created_at'] = comp['created_at']

# Merge with metrics
df = parsed.merge(metrics, on='company_id', how='left', suffixes=('', '_metrics'))

# Parse numeric fields
df['renewal_date'] = pd.to_datetime(df['renewal_date'])
df['health_score'] = pd.to_numeric(df['health_score'], errors='coerce')
df['acv_usd'] = pd.to_numeric(df['acv_usd'], errors='coerce')
df['created_at'] = pd.to_datetime(df['created_at'])

# Feature adoption % extraction
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['feature_adoption_pct'] = df['feature_adoption'].apply(extract_adoption_pct)

# Time since last value milestone
df['time_since_milestone_days'] = (df['renewal_date'] - df['created_at']).dt.days

# Communication & Interaction Features
df['avg_conversations_30d'] = df['contacts_active_30d']  # active contacts in 30 days
# Map sentiment_trend to numeric (higher = more negative)
sentiment_map = {'at-risk': 1.0, 'watch': 0.75, 'stable': 0.5, 'uplift': 0.25, 'positive': 0.0}
df['neg_sentiment_score'] = df['sentiment_trend'].map(sentiment_map).fillna(0.5)

# Support Experience Features
df['avg_resolution_time_min'] = df['p50_time_to_last_close_min']  # median time to close in minutes
df['reopen_proportion'] = df['p50_reopens']  # median reopens proportion

# Product Value Features
df['feature_adoption_coverage'] = df['feature_adoption_pct']  # already a percentage (0-100)

# Focus on target population
target = df[df['renewal_window'] == 'inside_90_days'].copy()
print(f"Target population (inside_90_days): {len(target)} companies")

# Outcome: expansion_signal
print("\nExpansion signal distribution (target):")
print(target['expansion_signal'].value_counts())

renewed = target[target['expansion_signal'] == 'Upsell Ready']
churned = target[target['expansion_signal'] == 'Risk Mitigation']
monitor = target[target['expansion_signal'] == 'Monitor']

print(f"\nRenewed (Upsell Ready): {len(renewed)}")
print(f"Churned (Risk Mitigation): {len(churned)}")

# Feature comparison
features = ['avg_conversations_30d', 'neg_sentiment_score', 'avg_resolution_time_min', 
            'reopen_proportion', 'feature_adoption_coverage', 'time_since_milestone_days',
            'health_score', 'acv_usd', 'total_conversations', 'p50_time_to_first_response_min',
            'registration_retention_30d']

print("\n=== Feature Comparison: Renewed vs Churned ===")
comparison_data = []
for feat in features:
    if feat in renewed.columns and feat in churned.columns:
        r_mean = renewed[feat].mean()
        c_mean = churned[feat].mean()
        r_std = renewed[feat].std()
        c_std = churned[feat].std()
        r_median = renewed[feat].median()
        c_median = churned[feat].median()
        diff = r_mean - c_mean
        pct_diff = (diff / max(abs(c_mean), 0.01)) * 100
        print(f"{feat:40s}: Renewed={r_mean:.3f}±{r_std:.3f} | Churned={c_mean:.3f}±{c_std:.3f} | Diff={diff:.3f} ({pct_diff:.1f}%)")
        comparison_data.append({
            'feature': feat, 'renewed_mean': r_mean, 'churned_mean': c_mean,
            'renewed_median': r_median, 'churned_median': c_median,
            'diff_mean': diff, 'diff_pct': pct_diff
        })

comp_df = pd.DataFrame(comparison_data)
print("\n\n=== Summary of differences ===")
print(comp_df.sort_values('diff_pct', key=abs, ascending=False).to_string())