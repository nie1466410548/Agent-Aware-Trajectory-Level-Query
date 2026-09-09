import pandas as pd

result = db.query("SELECT company_id, all_company_tags, created_at, updated_at FROM intercom__company_enhanced")
df = db.frame(result)

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(df['all_company_tags'].apply(parse_tags).tolist())
df = pd.concat([df, parsed], axis=1)

print("renewal_history sample:")
print(df['renewal_history'].dropna().head(20))

print("\nUnique renewal_history patterns:")
print(df['renewal_history'].unique()[:30])

print("\ncreated_at range:", df['created_at'].min(), df['created_at'].max())
print("updated_at range:", df['updated_at'].min(), df['updated_at'].max())

print("\nrenewal_date range:", df['renewal_date'].min(), df['renewal_date'].max())

# Check for any 'churn' references
churn_rows = df[df['all_company_tags'].str.contains('churn', case=False, na=False)]
print("\nRows mentioning churn:", len(churn_rows))

# Feature adoption
print("\nfeature_adoption distribution:")
print(df['feature_adoption'].value_counts())

print("\nsentiment_trend distribution:")
print(df['sentiment_trend'].value_counts())

print("\nlast_value_milestone distribution:")
print(df['last_value_milestone'].value_counts())