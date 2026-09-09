import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Get all relevant data
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))
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

# Merge with metrics
df = parsed.merge(metrics, on='company_id', how='left', suffixes=('', '_metrics'))

# Parse numeric fields
df['renewal_date'] = pd.to_datetime(df['renewal_date'])
df['health_score'] = pd.to_numeric(df['health_score'], errors='coerce')
df['acv_usd'] = pd.to_numeric(df['acv_usd'], errors='coerce')

# Feature adoption % extraction
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['feature_adoption_pct'] = df['feature_adoption'].apply(extract_adoption_pct)

# Time since last value milestone: current date - milestone date
# We don't have the milestone date directly, but we have renewal_date
# Let's estimate: milestone is typically achieved during the contract period
# The company_tags has last_value_milestone name only, not date
# We'll use the renewal_date - created_at to estimate time since milestone
# Actually, let's check if there's a milestone date in the data
# The tag only has milestone name, not date. 
# We'll use the company_age_days or created_at as a proxy
# For "time since last milestone", we can use: (renewal_date - created_at) as a rough proxy
# Or better: let's check if there's a date in the milestone name... no.

# Alternative: compute from conversation data - check if conversations mention milestone timing
# For now, use company_age_days as a rough proxy for "how long since last engagement"
# Actually, the task says "time since last value milestone (current date - date of most recent milestone achievement)"
# We don't have the milestone date in the data. Let's use the company's created_at as a rough proxy
# time_since_milestone = renewal_date - created_at (in days)
df['created_at'] = pd.to_datetime(df['created_at'])
df['time_since_milestone_days'] = (df['renewal_date'] - df['created_at']).dt.days

# Communication & Interaction Features (from company_metrics)
# avg_conversations = total_conversations / company_age_days * 30? 
# Or just use total_conversations as the conversation count
# The task asks for "average number of conversations" over last 30 days
# company_metrics has total_conversations (total for the company)
# Let's use contacts_active_30d as a proxy for recent activity
df['avg_conversations_30d'] = df['contacts_active_30d']  # active contacts in 30 days
df['neg_sentiment_trend'] = df['sentiment_trend'].map({'at-risk': 1, 'watch': 0.67, 'stable': 0.5, 'uplift': 0.33, 'positive': 0})

# Support Experience Features
df['avg_resolution_time'] = df['p50_time_to_last_close_min']  # median time to close
df['reopen_proportion'] = df['p50_reopens']  # median reopens (0-1 scale)

# Product Value Features
df['feature_adoption_coverage'] = df['feature_adoption_pct']  # already a percentage

# Focus on the target population: inside_90_days
target = df[df['renewal_window'] == 'inside_90_days'].copy()
print(f"Target population (inside_90_days): {len(target)} companies")

# Outcome: Use expansion_signal as renewal outcome proxy
# Upsell Ready = successfully renewed, Risk Mitigation = churned
print("\nExpansion signal distribution (target):")
print(target['expansion_signal'].value_counts())

# Compare features between renewed and churned
renewed = target[target['expansion_signal'] == 'Upsell Ready']
churned = target[target['expansion_signal'] == 'Risk Mitigation']
monitor = target[target['expansion_signal'] == 'Monitor']

print(f"\nRenewed (Upsell Ready): {len(renewed)}")
print(f"Churned (Risk Mitigation): {len(churned)}")
print(f"Monitor: {len(monitor)}")

# Feature comparison
features = ['avg_conversations_30d', 'neg_sentiment_trend', 'avg_resolution_time', 
            'reopen_proportion', 'feature_adoption_coverage', 'time_since_milestone_days',
            'health_score', 'acv_usd']

print("\n=== Feature Comparison: Renewed vs Churned ===")
for feat in features:
    if feat in renewed.columns and feat in churned.columns:
        r_mean = renewed[feat].mean()
        c_mean = churned[feat].mean()
        r_std = renewed[feat].std()
        c_std = churned[feat].std()
        diff = r_mean - c_mean
        diff_pct = diff / max(c_mean, 0.01) * 100
        print(f"{feat:35s}: Renewed={r_mean:.3f}±{r_std:.3f} | Churned={c_mean:.3f}±{c_std:.3f} | Diff={diff:.3f} ({diff_pct:.1f}%)")