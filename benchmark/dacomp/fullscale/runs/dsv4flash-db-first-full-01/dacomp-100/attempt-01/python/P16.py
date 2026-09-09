import pandas as pd
import numpy as np
from datetime import timedelta

# Get company data
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

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
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])
parsed['health_score'] = pd.to_numeric(parsed['health_score'], errors='coerce')
parsed['acv_usd'] = pd.to_numeric(parsed['acv_usd'], errors='coerce')

# Get conversation data with enhanced and metrics
conv_enh = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv_metrics = db.frame(db.query("""
    SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes, 
           conversation_created_at, conversation_last_updated_at
    FROM intercom__conversation_metrics
"""))

conv_enh['date'] = pd.to_datetime(conv_enh['conversation_created_at'])
conv_all = conv_enh.merge(conv_metrics, on='conversation_id', how='left', suffixes=('', '_m'))

# Parse sentiment from conversation tags
def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None

conv_all['sentiment'] = conv_all['all_conversation_tags'].apply(parse_sentiment)
# Define negative sentiments: escalation, risk_mitigation, cautious_watch, executive_focus
negative_sentiments = ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']
conv_all['is_negative'] = conv_all['sentiment'].isin(negative_sentiments)

# Resolution time from close_time - creation_time
# time_to_last_close_minutes is already the close time diff in minutes
conv_all['resolution_time_min'] = conv_all['time_to_last_close_minutes'].fillna(conv_all['time_to_first_close_minutes'])
conv_all['is_reopened'] = conv_all['count_reopens'] > 0

# Focus on within_30_days_past (historical renewal cycle)
past_companies = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
print(f"Within 30 days past: {len(past_companies)} companies")

# For each company, compute features from conversations in the 30 days before renewal
results = []
for idx, comp_row in past_companies.iterrows():
    cname = comp_row['company_name']
    ren_date = comp_row['renewal_date']
    window_start = ren_date - timedelta(days=30)
    
    # Get conversations for this company name in the 30-day window
    convs = conv_all[
        (conv_all['all_contact_company_names'] == cname) & 
        (conv_all['date'] >= window_start) &
        (conv_all['date'] < ren_date)
    ]
    
    n_convs = len(convs)
    avg_convs = n_convs  # count in last 30 days
    neg_prop = convs['is_negative'].mean() if n_convs > 0 else np.nan
    avg_res_time = convs['resolution_time_min'].mean() if n_convs > 0 else np.nan
    reopen_prop = convs['is_reopened'].mean() if n_convs > 0 else np.nan
    
    results.append({
        'company_id': comp_row['company_id'],
        'company_name': cname,
        'renewal_date': ren_date,
        'contract_size': comp_row['contract_size'],
        'industry': comp_row['industry'],
        'expansion_signal': comp_row['expansion_signal'],
        'health_score': comp_row['health_score'],
        'acv_usd': comp_row['acv_usd'],
        'feature_adoption': comp_row['feature_adoption'],
        'sentiment_trend': comp_row['sentiment_trend'],
        'n_convs_30d': n_convs,
        'avg_conversations_30d': avg_convs,
        'neg_sentiment_proportion': neg_prop,
        'avg_resolution_time_min': avg_res_time,
        'reopen_proportion': reopen_prop
    })

features_df = pd.DataFrame(results)
print(f"Companies with conversations in 30d window: {(features_df['n_convs_30d'] > 0).sum()}")
print(f"Companies with no conversations: {(features_df['n_convs_30d'] == 0).sum()}")

# For companies with no conversations, use the full 2023 conversation period as proxy
# (the last 30 days of available data)
print("\n\nUsing full 2023 conversation data as proxy for companies without 30d window...")
for idx, row in features_df[features_df['n_convs_30d'] == 0].iterrows():
    cname = row['company_name']
    # Use last 30 days of 2023 (Dec 2023)
    window_start = pd.Timestamp('2023-12-01')
    window_end = pd.Timestamp('2023-12-31')
    
    convs = conv_all[
        (conv_all['all_contact_company_names'] == cname) & 
        (conv_all['date'] >= window_start) &
        (conv_all['date'] <= window_end)
    ]
    
    n_convs = len(convs)
    avg_convs = n_convs
    neg_prop = convs['is_negative'].mean() if n_convs > 0 else 0.5
    avg_res_time = convs['resolution_time_min'].mean() if n_convs > 0 else np.nan
    reopen_prop = convs['is_reopened'].mean() if n_convs > 0 else 0
    
    features_df.at[idx, 'n_convs_30d'] = n_convs
    features_df.at[idx, 'avg_conversations_30d'] = avg_convs
    features_df.at[idx, 'neg_sentiment_proportion'] = neg_prop
    features_df.at[idx, 'avg_resolution_time_min'] = avg_res_time
    features_df.at[idx, 'reopen_proportion'] = reopen_prop

print(f"Companies with data after 2023 proxy: {(features_df['avg_conversations_30d'] > 0).sum()}")
print(f"Companies still without data: {(features_df['avg_conversations_30d'] == 0).sum()}")

# Now compare renewed vs churned
renewed = features_df[features_df['expansion_signal'] == 'Upsell Ready']
churned = features_df[features_df['expansion_signal'] == 'Risk Mitigation']
print(f"\nRenewed: {len(renewed)}, Churned: {len(churned)}")

compare_feats = ['avg_conversations_30d', 'neg_sentiment_proportion', 'avg_resolution_time_min', 'reopen_proportion']
print("\n=== Feature Comparison (from conversation data) ===")
for feat in compare_feats:
    r_mean = renewed[feat].mean()
    c_mean = churned[feat].mean()
    r_med = renewed[feat].median()
    c_med = churned[feat].median()
    r_std = renewed[feat].std()
    c_std = churned[feat].std()
    print(f"{feat:35s}: Renewed={r_mean:.3f}±{r_std:.3f} (med={r_med:.3f}) | Churned={c_mean:.3f}±{c_std:.3f} (med={c_med:.3f})")

# Also include feature adoption and time since milestone
# Feature adoption coverage from tags
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None

features_df['feature_adoption_coverage'] = features_df['feature_adoption'].apply(extract_adoption_pct)

# Time since last milestone - from company tags (last_value_milestone name + renewal_date)
# We don't have the milestone date, but we can use created_at as a rough proxy
# Actually, let's check if company_enhanced has a field for milestone
# For now, compute as: renewal_date - created_at (from company_enhanced)
comp_created = db.frame(db.query("SELECT company_id, created_at FROM intercom__company_enhanced"))
comp_created['created_at'] = pd.to_datetime(comp_created['created_at'])
features_df = features_df.merge(comp_created, on='company_id', how='left')
features_df['time_since_milestone_days'] = (features_df['renewal_date'] - features_df['created_at']).dt.days

print("\n\n=== Product Value Feature Comparison ===")
for feat in ['feature_adoption_coverage', 'time_since_milestone_days']:
    r_mean = renewed[feat].mean()
    c_mean = churned[feat].mean()
    r_med = renewed[feat].median()
    c_med = churned[feat].median()
    print(f"{feat:35s}: Renewed={r_mean:.3f} (med={r_med:.3f}) | Churned={c_mean:.3f} (med={c_med:.3f})")