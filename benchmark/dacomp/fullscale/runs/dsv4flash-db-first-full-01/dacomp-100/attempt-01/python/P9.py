import pandas as pd

# Get conversations for one company name
conv = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced"))

comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

# company parsed
parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])
parsed['company_name'] = comp['company_name']
parsed['company_id'] = comp['company_id']

# For a sample name, look at company_ids renewal dates
name = 'Atlas Dynamics'
sample = parsed[parsed['company_name'] == name]
print(f"Company_ids for {name}: {len(sample)}")
print(sample[['company_id', 'renewal_date', 'renewal_window', 'contract_size']].sort_values('renewal_date').head(40).to_string())

# Conversations for this name
conv_name = conv[conv['all_contact_company_names'] == name]
print(f"\nConversations for {name}: {len(conv_name)}")
print(conv_name['conversation_created_at'].sort_values().to_string())