import pandas as pd

comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])
parsed['acv_usd'] = pd.to_numeric(parsed['acv_usd'], errors='coerce')

print("Renewal date range by window:")
print(parsed.groupby('renewal_window')['renewal_date'].agg(['min', 'max', 'count']))

# Check what date is 90 days before the max inside_90_days renewal date
inside = parsed[parsed['renewal_window'] == 'inside_90_days']
print("\ninside_90_days renewal dates:")
print(inside['renewal_date'].describe())

past = parsed[parsed['renewal_window'] == 'within_30_days_past']
print("\nwithin_30_days_past renewal dates:")
print(past['renewal_date'].describe())

future = parsed[parsed['renewal_window'] == 'future_90_plus']
print("\nfuture_90_plus renewal dates:")
print(future['renewal_date'].describe())

# Check conversation date range
conv = db.frame(db.query("SELECT MIN(conversation_created_at) AS mn, MAX(conversation_created_at) AS mx, COUNT(*) AS n FROM intercom__conversation_enhanced"))
print("\nConversation dates:", conv) 