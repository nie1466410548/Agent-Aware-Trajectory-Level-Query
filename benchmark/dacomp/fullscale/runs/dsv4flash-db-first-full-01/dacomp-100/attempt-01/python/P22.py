import pandas as pd
import numpy as np

# Company data for historical cohort
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
parsed['is_renewed'] = parsed['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})

# Tag-based features by outcome
print("=== Communication Cadence by outcome ===")
print(pd.crosstab(parsed[parsed['is_renewed'].notna()]['is_renewed'], 
                  parsed[parsed['is_renewed'].notna()]['communication_cadence']))

print("\n=== Playbook by outcome ===")
print(pd.crosstab(parsed[parsed['is_renewed'].notna()]['is_renewed'],
                  parsed[parsed['is_renewed'].notna()]['playbook']))

print("\n=== education_focus by outcome ===")
print(pd.crosstab(parsed[parsed['is_renewed'].notna()]['is_renewed'],
                  parsed[parsed['is_renewed'].notna()]['education_focus']))

# Conversation-level features
conv = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags, conversation_state, sla_name, sla_status, conversation_rating FROM intercom__conversation_metrics"))

# Join to company name then to outcome via within_30_days_past
# Note: multiple company_ids per name, use the outcome of the within_30_days_past record
past_outcome = parsed[parsed['renewal_window'] == 'within_30_days_past'].groupby('company_name')['is_renewed'].first()
conv['outcome'] = conv['all_contact_company_names'].map(past_outcome)
conv_hist = conv[conv['outcome'].notna()]

print("\n=== SLA status by outcome (historical cohort) ===")
print(pd.crosstab(conv_hist['outcome'], conv_hist['sla_status']))
print(pd.crosstab(conv_hist['outcome'], conv_hist['sla_status'], normalize='index'))

print("\n=== SLA name by outcome ===")
print(pd.crosstab(conv_hist['outcome'], conv_hist['sla_name'], normalize='index'))

print("\n=== Conversation rating by outcome ===")
print(conv_hist.groupby('outcome')['conversation_rating'].describe())

print("\n=== conversation_state by outcome ===")
print(pd.crosstab(conv_hist['outcome'], conv_hist['conversation_state'], normalize='index'))

# Which conversations are in the pre-renewal window for the historical cohort?
conv_enh = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at FROM intercom__conversation_enhanced"))
conv_enh['date'] = pd.to_datetime(conv_enh['conversation_created_at'])
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])
past_rows = parsed[parsed['renewal_window'] == 'within_30_days_past']

# For each historical company, check if conversation is within 30 days before renewal
# Focus on the last conversations before renewal
import datetime
for _, row in past_rows.head(5).iterrows():
    cname = row['company_name']
    ren = row['renewal_date']
    win_start = ren - datetime.timedelta(days=30)
    convs = conv_enh[(conv_enh['all_contact_company_names'] == cname) & (conv_enh['date'] < ren)]
    last_convs = convs.sort_values('date').tail(3)
    print(f"\n{cname} renewal={ren.date()} | last convs before renewal:")
    for _, c in last_convs.iterrows():
        print(f"   {c['date'].date()}")