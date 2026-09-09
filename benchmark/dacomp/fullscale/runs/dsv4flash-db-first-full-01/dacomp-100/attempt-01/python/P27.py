import pandas as pd
import numpy as np

comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags, company_age_days FROM intercom__company_enhanced"))
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
parsed['company_age_days'] = comp['company_age_days']

df = parsed.merge(metrics, on='company_id', how='left', suffixes=('', '_m'))
df['health_score'] = pd.to_numeric(df['health_score'], errors='coerce')
df['acv_usd'] = pd.to_numeric(df['acv_usd'], errors='coerce')
df['is_renewed'] = df['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
df = df.dropna(subset=['is_renewed'])
print(f"Full population with outcome proxy: {len(df)} ({df['is_renewed'].sum()} renewed, {(1-df['is_renewed']).sum()} churned)")

def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['adoption_pct'] = df['feature_adoption'].apply(extract_adoption_pct)

print("\n=== Feature adoption % by outcome (full pop) ===")
print(df.groupby('is_renewed')['adoption_pct'].describe())

print("\n=== Sentiment trend by outcome (full pop) ===")
print(pd.crosstab(df['is_renewed'], df['sentiment_trend']))

print("\n=== Communication cadence by outcome (full pop) ===")
print(pd.crosstab(df['is_renewed'], df['communication_cadence'], normalize='index'))

print("\n=== Education focus by outcome (full pop) ===")
print(pd.crosstab(df['is_renewed'], df['education_focus'], normalize='index'))

print("\n=== Last value milestone by outcome (full pop) ===")
print(pd.crosstab(df['is_renewed'], df['last_value_milestone'], normalize='index'))

# ACV by outcome
print("\n=== ACV by outcome (full pop) ===")
print(df.groupby('is_renewed')['acv_usd'].describe())

# company_age_days
print("\n=== company_age_days by outcome ===")
print(df.groupby('is_renewed')['company_age_days'].describe())

# Contract size by outcome
print("\n=== Contract size by outcome ===")
print(pd.crosstab(df['is_renewed'], df['contract_size'], normalize='index'))