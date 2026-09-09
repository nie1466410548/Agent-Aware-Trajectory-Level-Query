import pandas as pd
import numpy as np
from datetime import timedelta

# Manual AUC calculation
def compute_auc(y_true, y_score):
    """Compute AUC using the Wilcoxon-Mann-Whitney statistic"""
    # y_true: binary labels (1=renewed, 0=churned)
    # y_score: continuous scores (higher = more renewed)
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    # Mann-Whitney U statistic
    n_pos = len(pos)
    n_neg = len(neg)
    # Count how many pairs (pos > neg)
    # For efficiency, use sorting
    combined = np.concatenate([pos, neg])
    labels = np.concatenate([np.ones(n_pos), np.zeros(n_neg)])
    # Sort by score
    order = np.argsort(combined)
    sorted_labels = labels[order]
    # Rank of positive instances
    ranks = np.arange(1, len(combined) + 1)
    pos_ranks = ranks[sorted_labels == 1]
    U = pos_ranks.sum() - n_pos * (n_pos + 1) / 2
    AUC = U / (n_pos * n_neg)
    return AUC if AUC >= 0.5 else 1 - AUC

# Get all data
comp = db.frame(db.query("SELECT company_id, company_name, created_at, all_company_tags FROM intercom__company_enhanced"))
metrics = db.frame(db.query("SELECT * FROM intercom__company_metrics"))

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

df = parsed.merge(metrics, on='company_id', how='left', suffixes=('', '_m'))
df['renewal_date'] = pd.to_datetime(df['renewal_date'])
df['health_score'] = pd.to_numeric(df['health_score'], errors='coerce')
df['acv_usd'] = pd.to_numeric(df['acv_usd'], errors='coerce')
df['created_at'] = pd.to_datetime(df['created_at'])

def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['feature_adoption_coverage'] = df['feature_adoption'].apply(extract_adoption_pct)
df['time_since_milestone_days'] = (df['renewal_date'] - df['created_at']).dt.days
df['conv_rate_per_30d'] = df['total_conversations'] / df['company_age_days'].clip(lower=1) * 30
df['neg_sentiment_score'] = df['sentiment_trend'].map({
    'at-risk': 1.0, 'watch': 0.75, 'stable': 0.5, 'uplift': 0.25, 'positive': 0.0
}).fillna(0.5)
df['avg_resolution_time_min'] = df['p50_time_to_last_close_min']
df['reopen_proportion'] = df['p50_reopens']

# Historical cohort
past = df[df['renewal_window'] == 'within_30_days_past'].copy()
past['is_renewed'] = past['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
analysis = past.dropna(subset=['is_renewed']).copy()
print(f"Analysis: {len(analysis)} companies ({analysis['is_renewed'].sum()} renewed, {(1-analysis['is_renewed']).sum()} churned)")

# Conversation data for 30-day window
conv_enh = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv_enh['date'] = pd.to_datetime(conv_enh['conversation_created_at'])

def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None
conv_enh['sentiment'] = conv_enh['all_conversation_tags'].apply(parse_sentiment)
neg_sentiments = ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']
conv_enh['is_negative'] = conv_enh['sentiment'].isin(neg_sentiments)

# Get conversation metrics for resolution time
conv_metrics = db.frame(db.query("""
    SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes
    FROM intercom__conversation_metrics
"""))
conv_metrics['resolution_time_min'] = conv_metrics['time_to_last_close_minutes'].fillna(conv_metrics['time_to_first_close_minutes'])
conv_metrics['is_reopened'] = conv_metrics['count_reopens'] > 0

conv_all = conv_enh.merge(conv_metrics, on='conversation_id', how='left')

# Compute conversation features for each company in 30-day window
conv_features = []
for _, row in analysis.iterrows():
    cname = row['company_name']
    ren_date = row['renewal_date']
    win_start = ren_date - timedelta(days=30)
    
    convs = conv_all[
        (conv_all['all_contact_company_names'] == cname) &
        (conv_all['date'] >= win_start) &
        (conv_all['date'] < ren_date)
    ]
    
    n = len(convs)
    neg_prop = convs['is_negative'].mean() if n > 0 else np.nan
    avg_res = convs['resolution_time_min'].mean() if n > 0 else np.nan
    reopen_prop = convs['is_reopened'].mean() if n > 0 else np.nan
    
    conv_features.append({
        'company_id': row['company_id'],
        'conv_count_30d': n,
        'neg_sent_prop_30d': neg_prop,
        'avg_res_time_30d': avg_res,
        'reopen_prop_30d': reopen_prop
    })

conv_df = pd.DataFrame(conv_features)
analysis = analysis.merge(conv_df, on='company_id', how='left')

# Features to evaluate
feature_defs = {
    'conv_count_30d': 'Avg Conversations (30d window)',
    'neg_sent_prop_30d': 'Negative Sentiment Proportion (30d)',
    'avg_res_time_30d': 'Avg Resolution Time (30d, min)',
    'reopen_prop_30d': 'Reopen Proportion (30d)',
    'neg_sentiment_score': 'Negative Sentiment Score (tag)',
    'feature_adoption_coverage': 'Feature Adoption Coverage (%)',
    'time_since_milestone_days': 'Time Since Milestone (days)',
    'avg_resolution_time_min': 'Median Resolution Time (company_metrics)',
    'reopen_proportion': 'Median Reopen Proportion (company_metrics)',
    'conv_rate_per_30d': 'Conversation Rate (per 30d)',
    'health_score': 'Health Score (composite)',
    'total_conversations': 'Total Conversations',
    'contacts_active_30d': 'Active Contacts (30d)',
    'p50_time_to_first_response_min': 'Time to First Response (min)',
    'registration_retention_30d': 'Registration Retention 30d'
}

results = []
for feat, label in feature_defs.items():
    if feat not in analysis.columns:
        continue
    data = analysis[['is_renewed', feat]].dropna()
    if len(data) < 10:
        continue
    
    y = data['is_renewed'].values.astype(int)
    X = data[feat].values.astype(float)
    
    # AUC (higher score = more renewed)
    auc = compute_auc(y, X)
    
    renewed_vals = data[data['is_renewed'] == 1][feat]
    churned_vals = data[data['is_renewed'] == 0][feat]
    
    # Quantile differences
    r_q25, r_q50, r_q75 = renewed_vals.quantile(0.25), renewed_vals.median(), renewed_vals.quantile(0.75)
    c_q25, c_q50, c_q75 = churned_vals.quantile(0.25), churned_vals.median(), churned_vals.quantile(0.75)
    
    results.append({
        'feature': label,
        'AUC': auc,
        'renewed_median': r_q50,
        'churned_median': c_q50,
        'renewed_Q1_Q3': f"{r_q25:.1f}–{r_q75:.1f}",
        'churned_Q1_Q3': f"{c_q25:.1f}–{c_q75:.1f}",
        'n': len(data)
    })

results_df = pd.DataFrame(results).sort_values('AUC', ascending=False)
print("\n=== Discriminative Power (AUC) — All Features ===")
print(results_df.to_string(index=False))

# Bar chart of top features
import matplotlib.pyplot as plt

top = results_df.head(10)
plt.figure(figsize=(10, 6))
colors = ['#2ecc71' if auc >= 0.7 else '#f39c12' if auc >= 0.6 else '#e74c3c' for auc in top['AUC']]
plt.barh(range(len(top)), top['AUC'].values, color=colors)
plt.yticks(range(len(top)), top['feature'].values)
plt.xlabel('AUC')
plt.title('Feature Discriminative Power (Renewed vs Churned)')
plt.axvline(0.5, color='gray', linestyle='--', alpha=0.5)
plt.axvline(0.7, color='green', linestyle='--', alpha=0.3, label='AUC=0.7')
plt.axvline(0.6, color='orange', linestyle='--', alpha=0.3, label='AUC=0.6')
plt.legend()
plt.tight_layout()
plt.savefig('/work/feature_auc.png', dpi=100)
print("\nSaved figure: /work/feature_auc.png")