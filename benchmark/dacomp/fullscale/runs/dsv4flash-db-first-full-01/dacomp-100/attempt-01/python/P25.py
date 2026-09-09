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

past = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
past['is_renewed'] = past['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
past = past.dropna(subset=['is_renewed'])

# Outcome consistency within company name
outcome_by_name = past.groupby('company_name')['is_renewed'].agg(['count', 'mean'])
mixed = outcome_by_name[(outcome_by_name['mean'] > 0) & (outcome_by_name['mean'] < 1)]
print(f"Names in historical cohort: {len(outcome_by_name)}")
print(f"Names with MIXED outcomes: {len(mixed)}")
print(f"Names with uniform outcome: {len(outcome_by_name) - len(mixed)}")

# Check if outcome correlates with contract_size within a name
print("\n=== Does outcome correlate with contract size? ===")
sub = past[['company_name', 'is_renewed', 'contract_size', 'acv_usd']].copy()
sub['acv_usd'] = pd.to_numeric(sub['acv_usd'], errors='coerce')
# Check renewal rate by contract size
print(pd.crosstab(sub['is_renewed'], sub['contract_size'], normalize='columns'))

# Check within a name: do different contract sizes have different outcomes?
name = sub['company_name'].value_counts().index[0]
print(f"\nSample name: {name}")
print(sub[sub['company_name'] == name].sort_values('contract_size'))

# ACV by outcome
print("\n=== ACV by outcome ===")
print(sub.groupby('is_renewed')['acv_usd'].describe())

# contract size by outcome counts
print("\n=== Contract size counts by outcome ===")
print(pd.crosstab(sub['is_renewed'], sub['contract_size']))