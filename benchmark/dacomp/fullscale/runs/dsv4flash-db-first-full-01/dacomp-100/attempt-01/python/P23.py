import pandas as pd
import numpy as np

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

# Focus on historical cohort (within_30_days_past)
past = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
past['is_renewed'] = past['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
past = past.dropna(subset=['is_renewed'])

print(f"Historical cohort: {len(past)} companies")
print(f"  Renewed: {past['is_renewed'].sum()}")
print(f"  Churned: {(1-past['is_renewed']).sum()}")

# Tag features by outcome
print("\n=== education_focus by outcome ===")
print(pd.crosstab(past['is_renewed'], past['education_focus']))

print("\n=== communication_cadence by outcome ===")
print(pd.crosstab(past['is_renewed'], past['communication_cadence']))

print("\n=== playbook by outcome ===")
print(pd.crosstab(past['is_renewed'], past['playbook']))

print("\n=== pricing_pressure by outcome ===")
print(pd.crosstab(past['is_renewed'], past['pricing_pressure']))

# Feature adoption
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
past['adoption_pct'] = past['feature_adoption'].apply(extract_adoption_pct)
print("\n=== Feature adoption by outcome ===")
print(past.groupby('is_renewed')['adoption_pct'].describe())

# Health score
past['health_score'] = pd.to_numeric(past['health_score'], errors='coerce')
print("\n=== Health score by outcome ===")
print(past.groupby('is_renewed')['health_score'].describe())

# Long format: list all unique tag keys
print("\n\n=== All tag keys ===")
sample = past.iloc[0]['all_company_tags']
for pair in sample.split('|'):
    if '=' in pair:
        k, v = pair.split('=', 1)
        print(f"  {k}")

# Check acv_usd
past['acv_usd'] = pd.to_numeric(past['acv_usd'], errors='coerce')
print("\n=== ACV by outcome ===")
print(past.groupby('is_renewed')['acv_usd'].describe())

# Check contract_size
print("\n=== Contract size by outcome ===")
print(pd.crosstab(past['is_renewed'], past['contract_size']))

# Last value milestone
print("\n=== Last value milestone by outcome ===")
print(pd.crosstab(past['is_renewed'], past['last_value_milestone']))