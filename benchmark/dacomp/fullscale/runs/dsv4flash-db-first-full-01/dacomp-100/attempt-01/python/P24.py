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

# Which company names have conversations?
conv_names = db.frame(db.query("SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced"))
conv_name_set = set(conv_names['all_contact_company_names'])

past['has_conv'] = past['company_name'].isin(conv_name_set)
print("Historical cohort companies with conversations:", past['has_conv'].sum())
print("Historical cohort companies without conversations:", (~past['has_conv']).sum())

# Names in historical cohort
names_in_cohort = past['company_name'].unique()
print(f"\nUnique names in historical cohort: {len(names_in_cohort)}")
print(f"Names with conversations: {len(set(names_in_cohort) & conv_name_set)}")

# For names with conversations, check outcome distribution
sub = past[past['has_conv']]
print("\n=== Outcome distribution for names with conversations ===")
print(sub['is_renewed'].value_counts())

# Check outcome consistency within name
outcome_by_name = sub.groupby('company_name')['is_renewed'].agg(['n', 'mean'])
print("\nNames with mixed outcomes:", (outcome_by_name['mean'] > 0) & (outcome_by_name['mean'] < 1))
print(outcome_by_name[((outcome_by_name['mean'] > 0) & (outcome_by_name['mean'] < 1))].head(10))

# How many companies per name in cohort
print("\nCompanies per name in cohort (with conv):")
print(sub.groupby('company_name').size().describe())

# Check the conversation-based features computed at name level
# since conversation data is the same for all companies sharing a name
# Let's compare name-level feature aggregates by name-level outcome
name_outcome = sub.groupby('company_name')['is_renewed'].first()
print("\nName-level outcomes (first):")
print(name_outcome.value_counts())