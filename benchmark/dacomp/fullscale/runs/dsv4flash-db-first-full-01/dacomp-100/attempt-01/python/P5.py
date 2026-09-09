import pandas as pd

comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags, created_at, updated_at FROM intercom__company_enhanced"))

# Get the 75 conversation companies
conv = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_subject, conversation_rating_remark FROM intercom__conversation_enhanced"))
conv_companies = set(conv['all_contact_company_names'])

comp75 = comp[comp['company_name'].isin(conv_companies)]
print("Number of company table rows matching the 75:", len(comp75))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp75['all_company_tags'].apply(parse_tags).tolist())
print("\nrenewal_window among the 75:")
print(parsed['renewal_window'].value_counts())

print("\ncontract_size among the 75:")
print(parsed['contract_size'].value_counts())

print("\nindustry among the 75:")
print(parsed['industry'].value_counts())

print("\nhealth_score among the 75:")
print(pd.to_numeric(parsed['health_score'], errors='coerce').describe())

print("\nConversation subjects:")
print(conv['conversation_subject'].value_counts())

print("\nConversation remarks sample:")
print(conv['conversation_rating_remark'].dropna().unique()[:30])

# Check distinct remark values
print("\nAll distinct remarks:")
print(conv['conversation_rating_remark'].dropna().unique())