import pandas as pd
from datetime import timedelta

# Company data
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['company_name'] = comp['company_name']
parsed['company_id'] = comp['company_id']
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])

# Conversations
conv = db.frame(db.query("""
    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced
"""))
conv['date'] = pd.to_datetime(conv['conversation_created_at'])

# Check for a sample of within_30_days_past companies
past = parsed[parsed['renewal_window'] == 'within_30_days_past'].head(5)
for _, row in past.iterrows():
    cname = row['company_name']
    ren_date = row['renewal_date']
    window_start = ren_date - timedelta(days=30)
    
    convs = conv[
        (conv['all_contact_company_names'] == cname) &
        (conv['date'] >= window_start) &
        (conv['date'] < ren_date)
    ]
    print(f"{cname}: renewal={ren_date.date()}, window={window_start.date()} to {ren_date.date()}, convs={len(convs)}")

# Check for a sample of inside_90_days companies
inside = parsed[parsed['renewal_window'] == 'inside_90_days'].head(5)
for _, row in inside.iterrows():
    cname = row['company_name']
    ren_date = row['renewal_date']
    window_start = ren_date - timedelta(days=30)
    
    convs = conv[
        (conv['all_contact_company_names'] == cname) &
        (conv['date'] >= window_start) &
        (conv['date'] < ren_date)
    ]
    print(f"{cname}: renewal={ren_date.date()}, window={window_start.date()} to {ren_date.date()}, convs={len(convs)}")

# Total count across all
def count_pre_renewal_convs(row):
    convs = conv[
        (conv['all_contact_company_names'] == row['company_name']) &
        (conv['date'] >= row['renewal_date'] - timedelta(days=30)) &
        (conv['date'] < row['renewal_date'])
    ]
    return len(convs)

# Sample a subset
sample = parsed[parsed['renewal_window'] == 'within_30_days_past'].head(50).copy()
sample['pre_convs'] = sample.apply(count_pre_renewal_convs, axis=1)
print(f"\nWithin 30 days past - pre-renewal convs: {sample['pre_convs'].sum()} / {len(sample)} companies with convs")

sample2 = parsed[parsed['renewal_window'] == 'inside_90_days'].head(50).copy()
sample2['pre_convs'] = sample2.apply(count_pre_renewal_convs, axis=1)
print(f"Inside 90 days - pre-renewal convs: {sample2['pre_convs'].sum()} / {len(sample2)} companies with convs")