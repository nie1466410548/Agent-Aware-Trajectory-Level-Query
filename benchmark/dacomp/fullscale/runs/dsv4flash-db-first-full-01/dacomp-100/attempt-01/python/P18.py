import pandas as pd
import numpy as np

# Get company tags and sentiment trend
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

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

# Conversation data
conv = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv['date'] = pd.to_datetime(conv['conversation_created_at'])

def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None

conv['sentiment'] = conv['all_conversation_tags'].apply(parse_sentiment)

# Full-year 2023 sentiment proportion per company name
conv_2023 = conv[conv['date'].dt.year == 2023]
sent_by_company = conv_2023.groupby('all_contact_company_names')['sentiment'].value_counts(normalize=True).unstack(fill_value=0)

# Merge with company trend (unique company_name - but each name maps to many company_ids with same sentiment_trend?)
# Check if sentiment_trend is consistent per company name
trend_by_name = parsed.groupby('company_name')['sentiment_trend'].nunique()
print("Companies with multiple sentiment_trends:", (trend_by_name > 1).sum())
print(trend_by_name[trend_by_name > 1].head())

# Get a mapping of company name -> expansion_signal for within_30_days_past
past = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
# Check if expansion_signal varies within a company name
exp_by_name = past.groupby('company_name')['expansion_signal'].nunique()
print("\nWithin 30d past, companies with multiple expansion_signals:", (exp_by_name > 1).sum())

# Since each company name maps to multiple ids across windows, and expansion_signal may vary,
# let me look at the relationship between company-level sentiment proportions and the
# sentiment_trend of the within_30_days_past records of that name.

# For each name, take the sentiment_trend of its within_30_days_past records (assume consistent)
past_trend = past.groupby('company_name')['sentiment_trend'].first()
past_exp = past.groupby('company_name')['expansion_signal'].first()

combined = sent_by_company.join(past_trend.rename('sentiment_trend')).join(past_exp.rename('expansion_signal'))
combined = combined.dropna()

print(f"\nCompanies with within_30_days_past data: {len(combined)}")
print("\n=== Avg negative sentiment proportion by company sentiment_trend ===")
for s in ['at-risk', 'watch', 'stable', 'uplift', 'positive']:
    subset = combined[combined['sentiment_trend'] == s]
    if len(subset) > 0:
        for neg in ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']:
            if neg in subset.columns:
                print(f"  trend={s}: {neg}={subset[neg].mean():.3f}")

print("\n=== Avg negative sentiment (3-cat) by company expansion_signal ===")
for exp in ['Risk Mitigation', 'Upsell Ready', 'Monitor']:
    subset = combined[combined['expansion_signal'] == exp]
    if len(subset) > 0:
        neg3 = subset.get('escalation', 0) + subset.get('risk_mitigation', 0) + subset.get('cautious_watch', 0)
        print(f"  exp={exp}: neg3_prop={neg3.mean():.3f}, n={len(subset)}")