import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve
from datetime import timedelta

# Get all data
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
df = parsed.merge(metrics, on='company_id', how='left', suffixes=('', '_m'))

# Parse fields
df['renewal_date'] = pd.to_datetime(df['renewal_date'])
df['health_score'] = pd.to_numeric(df['health_score'], errors='coerce')
df['acv_usd'] = pd.to_numeric(df['acv_usd'], errors='coerce')
df['created_at'] = pd.to_datetime(df['created_at'])

# Feature adoption % 
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['feature_adoption_coverage'] = df['feature_adoption'].apply(extract_adoption_pct)

# Time since last value milestone (days)
df['time_since_milestone_days'] = (df['renewal_date'] - df['created_at']).dt.days

# Communication & Interaction Features
# avg_conversations_30d: use total_conversations / company_age_days * 30 as a rate
# Or use contacts_active_30d as proxy for recent conversations
df['conv_rate_per_30d'] = df['total_conversations'] / df['company_age_days'].clip(lower=1) * 30
df['neg_sentiment_score'] = df['sentiment_trend'].map({
    'at-risk': 1.0, 'watch': 0.75, 'stable': 0.5, 'uplift': 0.25, 'positive': 0.0
}).fillna(0.5)

# Support Experience Features
df['avg_resolution_time_min'] = df['p50_time_to_last_close_min']  # median close time
df['reopen_proportion'] = df['p50_reopens']  # median reopens proportion

# Focus on historical cohort: within_30_days_past
past = df[df['renewal_window'] == 'within_30_days_past'].copy()

# Create binary outcome: 1 = Renewed (Upsell Ready), 0 = Churned (Risk Mitigation)
past['is_renewed'] = past['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
analysis = past.dropna(subset=['is_renewed']).copy()
print(f"Analysis sample: {len(analysis)} companies (renewed={analysis['is_renewed'].sum()}, churned={(1-analysis['is_renewed']).sum()})")

# Define features to evaluate
features = {
    'avg_conversations_30d': 'Conversation Rate (conv/30d)',
    'neg_sentiment_score': 'Negative Sentiment Score',
    'avg_resolution_time_min': 'Avg Resolution Time (min)',
    'reopen_proportion': 'Reopen Proportion',
    'feature_adoption_coverage': 'Feature Adoption Coverage (%)',
    'time_since_milestone_days': 'Time Since Milestone (days)',
    'health_score': 'Health Score',
    'acv_usd': 'ACV (USD)',
    'total_conversations': 'Total Conversations',
    'p50_time_to_first_response_min': 'Time to First Response (min)',
    'registration_retention_30d': 'Registration Retention 30d'
}

# Compute AUC and quantile differences
results = []
for feat, label in features.items():
    if feat not in analysis.columns:
        continue
    data = analysis[['is_renewed', feat]].dropna()
    if len(data) < 10:
        continue
    
    X = data[feat].values
    y = data['is_renewed'].values
    
    # AUC
    try:
        auc = roc_auc_score(y, X)
    except:
        auc = np.nan
    
    # Quantile difference (Q3-Q1 for renewed vs churned)
    renewed_vals = data[data['is_renewed'] == 1][feat]
    churned_vals = data[data['is_renewed'] == 0][feat]
    
    r_mean = renewed_vals.mean()
    c_mean = churned_vals.mean()
    r_med = renewed_vals.median()
    c_med = churned_vals.median()
    r_q1 = renewed_vals.quantile(0.25)
    r_q3 = renewed_vals.quantile(0.75)
    c_q1 = churned_vals.quantile(0.25)
    c_q3 = churned_vals.quantile(0.75)
    
    # Quantile difference (effect size)
    qdiff = (r_med - c_med) / max(c_q3 - c_q1, 1)
    
    results.append({
        'feature': feat,
        'label': label,
        'AUC': auc,
        'renewed_mean': r_mean,
        'churned_mean': c_mean,
        'renewed_median': r_med,
        'churned_median': c_med,
        'renewed_Q1_Q3': f"{r_q1:.1f}-{r_q3:.1f}",
        'churned_Q1_Q3': f"{c_q1:.1f}-{c_q3:.1f}",
        'quantile_diff': qdiff,
        'n': len(data)
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('AUC', ascending=False)
print("\n=== Feature Discriminative Power (AUC & Quantile Differences) ===")
print(results_df[['label', 'AUC', 'renewed_mean', 'churned_mean', 'quantile_diff']].to_string(index=False))

# Also compute the task-specific features properly
print("\n\n=== Task Features (Communication & Interaction) ===")
# avg conversations: we need to compute from conversation data
# Let's compute from the conversation data for the 30-day window
conv_enh = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv_enh['date'] = pd.to_datetime(conv_enh['conversation_created_at'])

# For each company in the analysis sample, get conversations in 30-day window before renewal
conv_features = []
for _, row in analysis.iterrows():
    cname = row['company_name']
    ren_date = row['renewal_date']
    win_start = ren_date - timedelta(days=30)
    
    convs = conv_enh[
        (conv_enh['all_contact_company_names'] == cname) &
        (conv_enh['date'] >= win_start) &
        (conv_enh['date'] < ren_date)
    ]
    
    conv_features.append({
        'company_id': row['company_id'],
        'conv_count_30d': len(convs),
        'has_conv_30d': len(convs) > 0
    })

conv_df = pd.DataFrame(conv_features)
analysis = analysis.merge(conv_df, on='company_id', how='left')

# For companies without 30d window conversations, use contact_active_30d
analysis['avg_conversations_30d_raw'] = np.where(
    analysis['has_conv_30d'], 
    analysis['conv_count_30d'], 
    analysis['contacts_active_30d']
)

# AUC for the raw conversation count
data = analysis[['is_renewed', 'avg_conversations_30d_raw']].dropna()
if len(data) > 10:
    auc_conv = roc_auc_score(data['is_renewed'], data['avg_conversations_30d_raw'])
    print(f"Avg conversations (from conv data + contacts_active_30d proxy): AUC = {auc_conv:.4f}")
    print(f"  Renewed mean: {data[data['is_renewed']==1]['avg_conversations_30d_raw'].mean():.2f}")
    print(f"  Churned mean: {data[data['is_renewed']==0]['avg_conversations_30d_raw'].mean():.2f}")

# Also compute avg conversations from total_conversations / age
data2 = analysis[['is_renewed', 'conv_rate_per_30d']].dropna()
auc_conv2 = roc_auc_score(data2['is_renewed'], data2['conv_rate_per_30d'])
print(f"\nConversation rate (total/age*30): AUC = {auc_conv2:.4f}")
print(f"  Renewed mean: {data2[data2['is_renewed']==1]['conv_rate_per_30d'].mean():.2f}")
print(f"  Churned mean: {data2[data2['is_renewed']==0]['conv_rate_per_30d'].mean():.2f}")