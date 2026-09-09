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
parsed['health_score'] = pd.to_numeric(parsed['health_score'], errors='coerce')

past = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
print(f"within_30_days_past: {len(past)}")

# Cross-tab expansion_signal vs sentiment_trend
print("\n=== expansion_signal vs sentiment_trend ===")
print(pd.crosstab(past['expansion_signal'], past['sentiment_trend']))

# Cross-tab expansion_signal vs health buckets
past['health_bucket'] = pd.cut(past['health_score'], bins=[0, 60, 70, 80, 100], labels=['<60', '60-70', '70-80', '80+'])
print("\n=== expansion_signal vs health_bucket ===")
print(pd.crosstab(past['expansion_signal'], past['health_bucket']))

# Feature adoption buckets
def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
past['adoption'] = past['feature_adoption'].apply(extract_adoption_pct)
past['adopt_bucket'] = pd.cut(past['adoption'], bins=[0, 60, 70, 80, 100], labels=['<60', '60-70', '70-80', '80+'])
print("\n=== expansion_signal vs adoption_bucket ===")
print(pd.crosstab(past['expansion_signal'], past['adopt_bucket']))

# health_score stats by expansion signal
print("\n=== health_score by expansion_signal ===")
print(past.groupby('expansion_signal')['health_score'].describe())

# Check pricing_pressure
print("\n=== expansion_signal vs pricing_pressure ===")
print(pd.crosstab(past['expansion_signal'], past['pricing_pressure']))