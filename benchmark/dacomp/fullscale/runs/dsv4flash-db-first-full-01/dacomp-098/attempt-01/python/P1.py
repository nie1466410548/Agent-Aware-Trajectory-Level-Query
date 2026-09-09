import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Read the full contact-level data
rows = []
with open('/results/S38.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)
df['first_conv_at'] = pd.to_datetime(df['first_conv_at'])
df['first_response_at'] = pd.to_datetime(df['first_response_at'])
df['demo_booked_at'] = pd.to_datetime(df['demo_booked_at'])
df['trial_activated_at'] = pd.to_datetime(df['trial_activated_at'])
df['paid_at'] = pd.to_datetime(df['paid_at'])

print(f"Total contacts: {len(df)}")
print(f"Bot first: {len(df[df['first_type']=='bot_first'])}")
print(f"Human first: {len(df[df['first_type']=='human_first'])}")
print()

# =============================================
# 1. CONVERSION RATES
# =============================================
print("="*60)
print("CONVERSION RATES BY FIRST RESPONSE TYPE")
print("="*60)

# Total contacts in each group
total_bot = len(df[df['first_type']=='bot_first'])
total_human = len(df[df['first_type']=='human_first'])
total_all = len(df)

# Reached demo
demo_bot = len(df[(df['first_type']=='bot_first') & (df['reached_demo']==1)])
demo_human = len(df[(df['first_type']=='human_first') & (df['reached_demo']==1)])
demo_all = len(df[df['reached_demo']==1])

# Reached trial (among those who reached demo)
trial_bot = len(df[(df['first_type']=='bot_first') & (df['reached_trial']==1)])
trial_human = len(df[(df['first_type']=='human_first') & (df['reached_trial']==1)])
trial_all = len(df[df['reached_trial']==1])

# Reached paid (among those who reached trial)
paid_bot = len(df[(df['first_type']=='bot_first') & (df['reached_paid']==1)])
paid_human = len(df[(df['first_type']=='human_first') & (df['reached_paid']==1)])
paid_all = len(df[df['reached_paid']==1])

print(f"\n[Stage 1: Conversation → Demo Booked]")
print(f"  Bot:   {demo_bot}/{total_bot} = {demo_bot/total_bot*100:.1f}%")
print(f"  Human: {demo_human}/{total_human} = {demo_human/total_human*100:.1f}%")
print(f"  All:   {demo_all}/{total_all} = {demo_all/total_all*100:.1f}%")

print(f"\n[Stage 2: Demo Booked → Trial Activated]")
print(f"  Bot:   {trial_bot}/{demo_bot} = {trial_bot/demo_bot*100:.1f}%")
print(f"  Human: {trial_human}/{demo_human} = {trial_human/demo_human*100:.1f}%")
print(f"  All:   {trial_all}/{demo_all} = {trial_all/demo_all*100:.1f}%")

print(f"\n[Stage 3: Trial Activated → Paid]")
print(f"  Bot:   {paid_bot}/{trial_bot} = {paid_bot/trial_bot*100:.1f}%")
print(f"  Human: {paid_human}/{trial_human} = {paid_human/trial_human*100:.1f}%")
print(f"  All:   {paid_all}/{trial_all} = {paid_all/trial_all*100:.1f}%")

# =============================================
# 2. STAGE DURATIONS
# =============================================
print("\n" + "="*60)
print("STAGE DURATIONS (average days)")
print("="*60)

# Duration 1: First response → Demo booked
# Only contacts with both first_response and demo_booked, and where demo_booked >= first_response
d1 = df[df['demo_booked_at'].notna() & df['first_response_at'].notna()].copy()
d1['dur_1'] = (d1['demo_booked_at'] - d1['first_response_at']).dt.total_seconds() / 86400
# Filter positive durations (where demo booking happened after first response)
d1_pos = d1[d1['dur_1'] >= 0]

for grp, label in [('bot_first', 'Bot'), ('human_first', 'Human')]:
    subset = d1_pos[d1_pos['first_type']==grp]
    if len(subset) > 0:
        print(f"  {label}: {subset['dur_1'].mean():.1f} days (n={len(subset)})")

# Duration 2: Demo booked → Trial activated
d2 = df[df['demo_booked_at'].notna() & df['trial_activated_at'].notna()].copy()
d2['dur_2'] = (d2['trial_activated_at'] - d2['demo_booked_at']).dt.total_seconds() / 86400
d2_pos = d2[d2['dur_2'] >= 0]

for grp, label in [('bot_first', 'Bot'), ('human_first', 'Human')]:
    subset = d2_pos[d2_pos['first_type']==grp]
    if len(subset) > 0:
        print(f"  {label}: {subset['dur_2'].mean():.1f} days (n={len(subset)})")

# Duration 3: Trial activated → Paid
d3 = df[df['trial_activated_at'].notna() & df['paid_at'].notna()].copy()
d3['dur_3'] = (d3['paid_at'] - d3['trial_activated_at']).dt.total_seconds() / 86400
d3_pos = d3[d3['dur_3'] >= 0]

for grp, label in [('bot_first', 'Bot'), ('human_first', 'Human')]:
    subset = d3_pos[d3_pos['first_type']==grp]
    if len(subset) > 0:
        print(f"  {label}: {subset['dur_3'].mean():.1f} days (n={len(subset)})")

# =============================================
# 3. BREAKDOWN BY INTENT
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY INTENT LABEL")
print("="*60)

intent_breakdown = df.groupby('intent').agg(
    total=('contact_id', 'count'),
    bot_first=('first_type', lambda x: (x=='bot_first').sum()),
    human_first=('first_type', lambda x: (x=='human_first').sum()),
    demo_rate=('reached_demo', 'mean'),
    trial_rate=('reached_trial', 'mean'),
    paid_rate=('reached_paid', 'mean')
).reset_index()

for _, row in intent_breakdown.sort_values('total', ascending=False).iterrows():
    print(f"  {row['intent']}: n={row['total']} (bot={row['bot_first']}, human={row['human_first']}) | Demo={row['demo_rate']*100:.1f}% | Trial={row['trial_rate']*100:.1f}% | Paid={row['paid_rate']*100:.1f}%")

# =============================================
# 4. BREAKDOWN BY TOPIC
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY TOPIC")
print("="*60)

topic_breakdown = df.groupby('topic').agg(
    total=('contact_id', 'count'),
    demo_rate=('reached_demo', 'mean'),
    trial_rate=('reached_trial', 'mean'),
    paid_rate=('reached_paid', 'mean')
).reset_index()

for _, row in topic_breakdown.sort_values('total', ascending=False).iterrows():
    print(f"  {row['topic']}: n={row['total']} | Demo={row['demo_rate']*100:.1f}% | Trial={row['trial_rate']*100:.1f}% | Paid={row['paid_rate']*100:.1f}%")

# =============================================
# 5. BREAKDOWN BY REGION
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY REGION")
print("="*60)

region_breakdown = df.groupby('region').agg(
    total=('contact_id', 'count'),
    demo_rate=('reached_demo', 'mean'),
    trial_rate=('reached_trial', 'mean'),
    paid_rate=('reached_paid', 'mean')
).reset_index()

for _, row in region_breakdown.sort_values('total', ascending=False).iterrows():
    print(f"  {row['region']}: n={row['total']} | Demo={row['demo_rate']*100:.1f}% | Trial={row['trial_rate']*100:.1f}% | Paid={row['paid_rate']*100:.1f}%")

# =============================================
# 6. INTERACTION: FIRST TYPE × INTENT
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY FIRST TYPE × INTENT")
print("="*60)

for intent in df['intent'].unique():
    subset = df[df['intent']==intent]
    bot = subset[subset['first_type']=='bot_first']
    human = subset[subset['first_type']=='human_first']
    if len(bot) == 0 or len(human) == 0:
        continue
    print(f"\n  Intent: {intent}")
    print(f"    Bot (n={len(bot)}):   Demo={bot['reached_demo'].mean()*100:.1f}% | Trial={bot['reached_trial'].mean()*100:.1f}% | Paid={bot['reached_paid'].mean()*100:.1f}%")
    print(f"    Human (n={len(human)}): Demo={human['reached_demo'].mean()*100:.1f}% | Trial={human['reached_trial'].mean()*100:.1f}% | Paid={human['reached_paid'].mean()*100:.1f}%")

# =============================================
# 7. INTERACTION: FIRST TYPE × TOPIC
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY FIRST TYPE × TOPIC")
print("="*60)

for topic in df['topic'].unique():
    subset = df[df['topic']==topic]
    bot = subset[subset['first_type']=='bot_first']
    human = subset[subset['first_type']=='human_first']
    if len(bot) == 0 or len(human) == 0:
        continue
    print(f"\n  Topic: {topic}")
    print(f"    Bot (n={len(bot)}):   Demo={bot['reached_demo'].mean()*100:.1f}% | Trial={bot['reached_trial'].mean()*100:.1f}% | Paid={bot['reached_paid'].mean()*100:.1f}%")
    print(f"    Human (n={len(human)}): Demo={human['reached_demo'].mean()*100:.1f}% | Trial={human['reached_trial'].mean()*100:.1f}% | Paid={human['reached_paid'].mean()*100:.1f}%")

# =============================================
# 8. INTERACTION: FIRST TYPE × REGION
# =============================================
print("\n" + "="*60)
print("CONVERSION RATES BY FIRST TYPE × REGION")
print("="*60)

for region in df['region'].unique():
    subset = df[df['region']==region]
    bot = subset[subset['first_type']=='bot_first']
    human = subset[subset['first_type']=='human_first']
    if len(bot) == 0 or len(human) == 0:
        continue
    print(f"\n  Region: {region}")
    print(f"    Bot (n={len(bot)}):   Demo={bot['reached_demo'].mean()*100:.1f}% | Trial={bot['reached_trial'].mean()*100:.1f}% | Paid={bot['reached_paid'].mean()*100:.1f}%")
    print(f"    Human (n={len(human)}): Demo={human['reached_demo'].mean()*100:.1f}% | Trial={human['reached_trial'].mean()*100:.1f}% | Paid={human['reached_paid'].mean()*100:.1f}%")