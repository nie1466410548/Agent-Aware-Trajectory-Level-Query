import pandas as pd
import numpy as np

# Load events and conversations again
event_sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_created_at,
         LEAD(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS next_created_at
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_created_at, next_created_at,
       prev_plan, plan_name AS new_plan,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
"""
events = db.frame(db.query(event_sql))
events['event_at'] = pd.to_datetime(events['event_at'])
events['prev_created_at'] = pd.to_datetime(events['prev_created_at'])
events['next_created_at'] = pd.to_datetime(events['next_created_at'])

conv_sql = """
SELECT all_contact_company_names as company_name, conversation_created_at, all_conversation_tags,
       sla_status, conversation_rating, conversation_subject
FROM intercom__conversation_enhanced
"""
convs = db.frame(db.query(conv_sql))
convs['conversation_created_at'] = pd.to_datetime(convs['conversation_created_at'])

# Restrict to companies with conversations
conv_companies = set(convs['company_name'].unique())
events_conv = events[events['company_name'].isin(conv_companies)].copy()

# For each event, collect before/after conversations (within the plan period windows)
tag_analysis = []
for _, ev in events_conv.iterrows():
    cn = ev['company_name']
    sub = convs[convs['company_name'] == cn]
    if len(sub) == 0:
        continue
    cmin = sub['conversation_created_at'].min()
    cmax = sub['conversation_created_at'].max()
    evt = ev['event_at']
    prev_start = max(ev['prev_created_at'], cmin) if pd.notna(ev['prev_created_at']) else cmin
    next_end = min(ev['next_created_at'], cmax) if pd.notna(ev['next_created_at']) else cmax
    
    before = sub[(sub['conversation_created_at'] >= prev_start) & (sub['conversation_created_at'] < evt)]
    after = sub[(sub['conversation_created_at'] > evt) & (sub['conversation_created_at'] <= next_end)]
    
    if len(before) == 0 and len(after) == 0:
        continue
    
    # Analyze tag composition
    for period, window in [('before', before), ('after', after)]:
        if len(window) == 0:
            continue
        tags = ','.join(window['all_conversation_tags'].dropna())
        for tag in ['Bug', 'Outage', 'Escalation', 'Billing', 'Renewal', 'Implementation', 'Training', 
                    'Adoption Risk', 'Usage Spike', 'Integration', 'Data Quality', 'Security', 
                    'Upgrade Opportunity', 'Downgrade Risk', 'Executive Attention', 'Automation', 'Enablement', 'Mobile']:
            tag_analysis.append({'event_key': cn + str(evt), 'event_type': ev['event_type'], 
                                 'period': period, 'tag': tag, 
                                 'count': window['all_conversation_tags'].str.contains(tag, na=False).sum(),
                                 'total': len(window)})

tagdf = pd.DataFrame(tag_analysis)

# Aggregate: average share of each tag by event type and period
tag_summary = tagdf.groupby(['event_type', 'period', 'tag']).agg({'count': 'sum', 'total': 'sum'}).reset_index()
tag_summary['share'] = tag_summary['count'] / tag_summary['total']

# Pivot to compare before/after shares
piv = tag_summary.pivot_table(index=['event_type', 'tag'], columns='period', values='share').reset_index()
piv['before_total'] = tag_summary.groupby(['event_type','tag'])['count'].sum().values  # not quite right
print("=== Tag share by event type and period (proportion of conversations with tag) ===")
print(piv.sort_values(['event_type', 'tag']).round(3).to_string())

# Let's look at raw counts per 100 conversations instead
tag_summary['per100'] = tag_summary['count'] / tag_summary['total'] * 100
pivot2 = tag_summary.pivot_table(index=['event_type', 'tag'], columns='period', values='per100').reset_index()
print("\n=== Tag frequency per 100 conversations ===")
print(pivot2.sort_values(['event_type', 'tag']).round(2).to_string())

# Focus on interesting signals - change in tag frequency from before to after
pivot3 = tag_summary.pivot_table(index=['event_type', 'tag'], columns='period', values='per100').reset_index()
pivot3['change'] = pivot3.get('after', 0) - pivot3.get('before', 0)
print("\n=== Largest before->after changes in tag frequency (per 100 convs) ===")
up = pivot3[pivot3['event_type']=='upgrade'].sort_values('change', key=abs, ascending=False)
dn = pivot3[pivot3['event_type']=='downgrade'].sort_values('change', key=abs, ascending=False)
print("\nUPGRADE events:")
print(up[['tag','before','after','change']].round(2).head(10).to_string())
print("\nDOWNGRADE events:")
print(dn[['tag','before','after','change']].round(2).head(10).to_string())