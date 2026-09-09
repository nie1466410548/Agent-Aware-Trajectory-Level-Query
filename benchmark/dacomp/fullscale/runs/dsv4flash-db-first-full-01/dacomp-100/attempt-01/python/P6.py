import pandas as pd

# Get company data for the 75 companies that have conversations
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
comp_parsed = pd.concat([comp[['company_id', 'company_name']], parsed], axis=1)

# Get conversation companies
conv = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_subject FROM intercom__conversation_enhanced"))

# Merge
conv_companies = set(conv['all_contact_company_names'])
comp_75 = comp_parsed[comp_parsed['company_name'].isin(conv_companies)]
print("Renewal window distribution among the 75:")
print(comp_75['renewal_window'].value_counts())

print("\nContract size distribution among the 75:")
print(comp_75['contract_size'].value_counts())

print("\nIndustry distribution among the 75:")
print(comp_75['industry'].value_counts())

print("\nExpansion signal among the 75:")
print(comp_75['expansion_signal'].value_counts())

print("\nHealth score among the 75:")
print(pd.to_numeric(comp_75['health_score'], errors='coerce').describe())

# Check if there's a negative/positive conversation remark pattern
# Let's get the last conversation per company before renewal
comp_75['renewal_date'] = pd.to_datetime(comp_75['renewal_date'])
comp_75['health_score'] = pd.to_numeric(comp_75['health_score'], errors='coerce')

# Check conversation remarks
conv_remarks = db.frame(db.query("SELECT conversation_id, conversation_rating_remark FROM intercom__conversation_metrics"))
print("\nConv remarks count:", len(conv_remarks))
print("Conversation remarks:", conv_remarks['conversation_rating_remark'].unique())