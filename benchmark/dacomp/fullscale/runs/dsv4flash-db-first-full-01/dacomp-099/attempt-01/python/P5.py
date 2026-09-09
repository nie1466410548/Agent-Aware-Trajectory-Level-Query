import pandas as pd
import numpy as np
from scipy import stats

# Load all conversations for the 31 companies (with company name)
conv_sql = """
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type,
       cm.count_total_parts, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced c
LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
"""
convs = db.frame(db.query(conv_sql))
convs['conversation_created_at'] = pd.to_datetime(convs['conversation_created_at'])
print("Conversations shape:", convs.shape)

# Load all events (from the snapshot-based detection)
event_sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
"""
events = db.frame(db.query(event_sql))
events['event_at'] = pd.to_datetime(events['event_at'])
print("Events shape:", events.shape)
print(events['event_type'].value_counts())

# For each event, compute window metrics
records = []
for _, ev in events.iterrows():
    cn = ev['company_name']
    evt = ev['event_at']
    sub = convs[convs['company_name'] == cn].copy()
    before = sub[(sub['conversation_created_at'] < evt) & (sub['conversation_created_at'] >= evt - pd.Timedelta(days=30))]
    after = sub[(sub['conversation_created_at'] > evt) & (sub['conversation_created_at'] <= evt + pd.Timedelta(days=30))]
    
    def summarize(window_df):
        if len(window_df) == 0:
            return dict(convs=0, parts=0, bugs=0, outages=0, escalations=0, sla=0, cust_init=0, rating=0, days=0)
        return dict(
            convs=len(window_df),
            parts=window_df['count_total_parts'].sum(),
            bugs=window_df['all_conversation_tags'].str.contains('Bug', na=False).sum(),
            outages=window_df['all_conversation_tags'].str.contains('Outage', na=False).sum(),
            escalations=window_df['all_conversation_tags'].str.contains('Escalation', na=False).sum(),
            sla=window_df['sla_status'].eq('breached').sum(),
            cust_init=window_df['conversation_initiated_type'].eq('customer_initiated').sum(),
            rating=window_df[window_df['conversation_rating']>0]['conversation_rating'].mean() if (window_df['conversation_rating']>0).any() else 0,
            days=0
        )
    
    b = summarize(before)
    a = summarize(after)
    # days observed: use company conversation min/max
    cmin = sub['conversation_created_at'].min()
    cmax = sub['conversation_created_at'].max()
    before_start = max(cmin, evt - pd.Timedelta(days=30))
    after_end = min(cmax, evt + pd.Timedelta(days=30))
    b['days'] = max((evt - before_start).days, 0)
    a['days'] = max((after_end - evt).days, 0)
    
    rec = {'company_name': cn, 'event_at': evt, 'event_type': ev['event_type'],
           'prev_plan': ev['prev_plan'], 'new_plan': ev['new_plan']}
    for k, v in b.items():
        rec[f'before_{k}'] = v
    for k, v in a.items():
        rec[f'after_{k}'] = v
    records.append(rec)

evdf = pd.DataFrame(records)
print("\nPer-event dataframe shape:", evdf.shape)
print(evdf['event_type'].value_counts())

# Check data coverage
print("\nEvents with at least 1 conversation in window:")
print((evdf['before_convs'] + evdf['after_convs'] > 0).value_counts())
print("\nUpgrade events with data:", (evdf[(evdf['event_type']=='upgrade') & (evdf['before_convs']+evdf['after_convs']>0)].shape))
print("Downgrade events with data:", (evdf[(evdf['event_type']=='downgrade') & (evdf['before_convs']+evdf['after_convs']>0)].shape))

evdf.to_csv('/work/event_windows.csv', index=False)
print("\nSaved to /work/event_windows.csv")
print(evdf[['company_name','event_at','event_type','prev_plan','new_plan','before_days','after_days','before_convs','after_convs']].to_string())