import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Get all needed data
conv_enh = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, 
           all_conversation_tags, conversation_subject
    FROM intercom__conversation_enhanced
"""))
conv_metrics = db.frame(db.query("""
    SELECT conversation_id, count_reopens, time_to_last_close_minutes,
           time_to_first_close_minutes, conversation_created_at, conversation_last_updated_at
    FROM intercom__conversation_metrics
"""))

comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

# Parse company tags
def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['company_name'] = comp['company_name']
parsed['company_id'] = comp['company_id']
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])
parsed['health_score'] = pd.to_numeric(parsed['health_score'], errors='coerce')

# Parse sentiment from conversation tags
def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None

conv_enh['sentiment'] = conv_enh['all_conversation_tags'].apply(parse_sentiment)

# Define negative sentiments
negative_sentiments = ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']
positive_sentiments = ['optimistic', 'value_build', 'steady_positive', 'data_required']

conv_enh['is_negative'] = conv_enh['sentiment'].isin(negative_sentiments)
conv_enh['is_positive'] = conv_enh['sentiment'].isin(positive_sentiments)

print("Sentiment distribution:")
print(conv_enh['sentiment'].value_counts())
print("\nNegative count:", conv_enh['is_negative'].sum())
print("Positive count:", conv_enh['is_positive'].sum())

# Merge with metrics
conv_all = conv_enh.merge(conv_metrics, on='conversation_id', how='left', suffixes=('', '_metrics'))
conv_all['resolution_time_min'] = conv_all['time_to_last_close_minutes'].fillna(conv_all['time_to_first_close_minutes'])
conv_all['is_reopened'] = conv_all['count_reopens'] > 0

# Now compute features for each company name
# We need to compute features for the "last 30 days" relative to each company's renewal date
# Since each company_name has multiple company_ids with different renewal dates,
# we'll compute features per company_name and then join to each company_id

# For "last 30 days" - we need a reference date. Let's use the median renewal date per company name
# Actually, for the inside_90_days group, the "current date" is the anchor.
# Let's use the date that is 30 days before the renewal.
# But since each company_id has a different renewal date, we'll compute features
# relative to each company_id's renewal date.

# Actually, let's simplify: compute features for each company name for the "last 30 days" 
# before the earliest renewal date among that company's inside_90_days contracts.
# Hmm, this is getting complex.

# Let me take a different approach. For each company_id in inside_90_days:
# 1. Find the company name
# 2. Look at conversations in the 30 days before that company_id's renewal date
# 3. Compute features

# First, let's focus on the 419 inside_90_days companies
inside_companies = parsed[parsed['renewal_window'] == 'inside_90_days'].copy()
print(f"\nInside 90 days companies: {len(inside_companies)}")

# For each company, compute features from conversations in the 30 days before renewal
# conv_all has company names, so we can filter by name and date range

results = []
for idx, comp_row in inside_companies.iterrows():
    cname = comp_row['company_name']
    ren_date = comp_row['renewal_date']
    window_start = ren_date - timedelta(days=30)
    
    # Get conversations for this company name in the 30-day window
    convs = conv_all[
        (conv_all['all_contact_company_names'] == cname) & 
        (conv_all['conversation_created_at'] >= window_start.strftime('%Y-%m-%d')) &
        (conv_all['conversation_created_at'] < ren_date.strftime('%Y-%m-%d'))
    ]
    
    if len(convs) == 0:
        results.append({
            'company_id': comp_row['company_id'],
            'company_name': cname,
            'renewal_date': ren_date,
            'contract_size': comp_row['contract_size'],
            'industry': comp_row['industry'],
            'expansion_signal': comp_row['expansion_signal'],
            'health_score': comp_row['health_score'],
            'avg_conversations': 0,
            'neg_sentiment_proportion': 0,
            'avg_resolution_time': None,
            'reopen_proportion': 0,
            'n_convs': 0
        })
        continue
    
    avg_convs = len(convs)  # absolute count in 30 days
    neg_prop = convs['is_negative'].mean() if len(convs) > 0 else 0
    avg_res_time = convs['resolution_time_min'].mean()
    reopen_prop = convs['is_reopened'].mean()
    
    results.append({
        'company_id': comp_row['company_id'],
        'company_name': cname,
        'renewal_date': ren_date,
        'contract_size': comp_row['contract_size'],
        'industry': comp_row['industry'],
        'expansion_signal': comp_row['expansion_signal'],
        'health_score': comp_row['health_score'],
        'avg_conversations': avg_convs,
        'neg_sentiment_proportion': neg_prop,
        'avg_resolution_time': avg_res_time,
        'reopen_proportion': reopen_prop,
        'n_convs': len(convs)
    })

features_df = pd.DataFrame(results)
print(f"\nComputed features for {len(features_df)} companies")
print(f"Companies with conversations: {features_df['n_convs'].sum()}")
print(f"Companies with at least 1 conv: {(features_df['n_convs'] > 0).sum()}")
print(features_df[['avg_conversations', 'neg_sentiment_proportion', 'avg_resolution_time', 'reopen_proportion']].describe())