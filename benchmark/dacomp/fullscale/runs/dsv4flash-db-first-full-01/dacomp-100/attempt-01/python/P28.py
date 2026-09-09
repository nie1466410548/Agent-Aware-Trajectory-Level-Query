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

def extract_adoption_pct(x):
    try:
        return float(x.split('(')[1].split('%')[0])
    except:
        return None
df['adoption_pct'] = df['feature_adoption'].apply(extract_adoption_pct)

# Risk score: sentiment_trend at-risk/watch + health_score < 70
df['risk_level'] = 'Monitor'
df.loc[(df['sentiment_trend'].isin(['at-risk', 'watch'])) | (df['health_score'] < 70), 'risk_level'] = 'At-Risk'
df.loc[(df['sentiment_trend'].isin(['positive', 'uplift', 'stable'])) & (df['health_score'] >= 70), 'risk_level'] = 'Low-Risk'

# Target population
target = df[df['renewal_window'] == 'inside_90_days'].copy()
print(f"Target population (renewal within 90 days): {len(target)}")
print("\nRisk level distribution:")
print(target['risk_level'].value_counts())

# At-risk rate by industry
print("\n=== At-Risk Rate by Industry (target population) ===")
target['is_at_risk'] = (target['risk_level'] == 'At-Risk').astype(int)
industry_risk = target.groupby('industry').agg(
    n=('company_id', 'count'),
    at_risk=('is_at_risk', 'sum'),
    at_risk_rate=('is_at_risk', 'mean'),
    avg_health=('health_score', 'mean'),
    avg_adoption=('adoption_pct', 'mean')
).sort_values('at_risk_rate', ascending=False)
print(industry_risk.to_string())

print("\n=== At-Risk Rate by Contract Size (target population) ===")
size_risk = target.groupby('contract_size').agg(
    n=('company_id', 'count'),
    at_risk=('is_at_risk', 'sum'),
    at_risk_rate=('is_at_risk', 'mean'),
    avg_health=('health_score', 'mean'),
    avg_adoption=('adoption_pct', 'mean')
).sort_values('at_risk_rate', ascending=False)
print(size_risk.to_string())

# Cross-tab industry x contract size
print("\n=== At-risk rate by industry x contract size ===")
cross = target.pivot_table(index='industry', columns='contract_size', values='is_at_risk', aggfunc='mean')
print(cross.round(2).to_string())

# Revenue at risk (ACV sum)
print("\n=== ACV at risk by industry ===")
industry_risk['acv_at_risk'] = target.groupby('industry').apply(
    lambda x: x.loc[x['is_at_risk'] == 1, 'acv_usd'].sum(), include_groups=False
)
industry_risk = industry_risk.sort_values('acv_at_risk', ascending=False)
print(industry_risk[['n', 'at_risk', 'at_risk_rate', 'acv_at_risk']].to_string())

# Save target population data
target[['company_id', 'company_name', 'industry', 'contract_size', 'acv_usd', 'health_score', 
        'sentiment_trend', 'adoption_pct', 'expansion_signal', 'risk_level']].to_csv('/work/target_population.csv', index=False)