import pandas as pd

conv = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv['date'] = pd.to_datetime(conv['conversation_created_at'])
conv['year'] = conv['date'].dt.year

# How many companies have 2023 vs 2029 conversations?
year_counts = conv.groupby(['all_contact_company_names', 'year']).size().unstack(fill_value=0)
print("Company-year distribution:")
print(year_counts.describe())
print("\nCompanies with only 2023:", (year_counts.get(2029, 0) == 0).sum())
print("Companies with only 2029:", (year_counts.get(2023, 0) == 0).sum())
print("Companies with both:", ((year_counts.get(2023, 0) > 0) & (year_counts.get(2029, 0) > 0)).sum())

# Parse sentiment
def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None

conv['sentiment'] = conv['all_conversation_tags'].apply(parse_sentiment)
negative = ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']

# For each company, compute negative sentiment proportion by year
conv['is_neg'] = conv['sentiment'].isin(negative)
company_neg = conv.groupby(['all_contact_company_names', 'year']).agg(
    n=('conversation_id', 'count'),
    neg_prop=('is_neg', 'mean')
).reset_index()

print("\nTop companies by 2023 negative sentiment proportion:")
print(company_neg[company_neg['year']==2023].sort_values('neg_prop', ascending=False).head(10).to_string())
print("\nBottom companies by 2023 negative sentiment proportion:")
print(company_neg[company_neg['year']==2023].sort_values('neg_prop').head(10).to_string())