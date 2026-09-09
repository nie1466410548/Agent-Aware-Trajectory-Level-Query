import pandas as pd
import json

# Get all company data
result = db.query("SELECT * FROM intercom__company_enhanced")
df = db.frame(result)

# Parse tags
def parse_tags(tags_str):
    d = {}
    pairs = tags_str.split('|')
    for pair in pairs:
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = df['all_company_tags'].apply(parse_tags)
tags_df = pd.DataFrame(parsed.tolist())
print("All tag keys:", list(tags_df.columns))

# Show value distribution for key fields
for col in ['renewal_window', 'contract_size', 'industry', 'contract_tier', 'segment', 'expansion_signal']:
    if col in tags_df.columns:
        print(f"\n{col} distribution:")
        print(tags_df[col].value_counts())

# Check renewal dates
print("\nRenewal dates sample:")
print(tags_df['renewal_date'].head(10))
print("\nUnique renewal windows:", tags_df['renewal_window'].unique())