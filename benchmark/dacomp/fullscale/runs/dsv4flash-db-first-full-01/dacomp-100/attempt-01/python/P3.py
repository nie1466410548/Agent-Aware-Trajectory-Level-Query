import pandas as pd

# Get all conversation tags
result = db.query("SELECT conversation_id, all_conversation_tags, all_contact_company_names FROM intercom__conversation_enhanced")
df = db.frame(result)

# Parse sentiment from tags
def parse_tag_value(tags_str, key):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == key:
                return v.strip()
    return None

sentiments = df['all_conversation_tags'].apply(lambda x: parse_tag_value(x, 'sentiment'))
print("Distinct sentiments in conversation tags:")
print(sentiments.value_counts())

# Topics
topics = df['all_conversation_tags'].apply(lambda x: parse_tag_value(x, 'topic'))
print("\nDistinct topics:")
print(topics.value_counts())

# Check company names
print("\nUnique company names count:", df['all_contact_company_names'].nunique())

# Now let's look at the relationship between renewal_window and other signals
result2 = db.query("SELECT all_company_tags FROM intercom__company_enhanced")
df2 = db.frame(result2)
parsed = pd.DataFrame(df2['all_company_tags'].apply(lambda x: {pair.split('=')[0].strip(): pair.split('=')[1].strip() for pair in x.split('|') if '=' in pair}).tolist())

# Check if renewal_window correlates with expansion_signal, health_score, etc.
print("\n=== Cross-tab: renewal_window vs expansion_signal ===")
print(pd.crosstab(parsed['renewal_window'], parsed['expansion_signal']))

print("\n=== Cross-tab: renewal_window vs sentiment_trend ===")
print(pd.crosstab(parsed['renewal_window'], parsed['sentiment_trend']))

print("\n=== Cross-tab: renewal_window vs contract_size ===")
print(pd.crosstab(parsed['renewal_window'], parsed['contract_size']))

# Check health_score by renewal_window
print("\n=== health_score stats by renewal_window ===")
parsed['health_score'] = pd.to_numeric(parsed['health_score'], errors='coerce')
print(parsed.groupby('renewal_window')['health_score'].describe())

# feature_adoption - extract numeric value
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None

parsed['adoption_pct'] = parsed['feature_adoption'].apply(extract_adoption_pct)
print("\n=== adoption_pct stats by renewal_window ===")
print(parsed.groupby('renewal_window')['adoption_pct'].describe())