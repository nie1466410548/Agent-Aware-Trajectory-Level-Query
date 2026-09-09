import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/work/contact_funnel.csv')
print(f"Total contacts: {len(df)}")
print(f"Bot first: {len(df[df['first_type']=='bot_first'])}")
print(f"Human first: {len(df[df['first_type']=='human_first'])}")
print()

# ============ BREAKDOWN BY INTENT ============
print("="*80)
print("CONVERSION RATES BY FIRST TYPE × INTENT")
print("="*80)

for intent in sorted(df['intent'].unique()):
    sub = df[df['intent']==intent]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb==0 or nh==0:
        print(f"\n{intent:20s}: only {'bot' if nb>0 else 'human'} (n={nb+nh})")
        continue
    db, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{intent:20s}  Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':20s}  {db/nb*100:5.1f}%           {dh/nh*100:5.1f}%")
    if db>0: print(f"  {'Trial rate:':20s}  {tb/db*100:5.1f}%           {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':20s}  {pb/tb*100:5.1f}%           {ph/th*100:5.1f}%")

# ============ BREAKDOWN BY TOPIC ============
print("\n" + "="*80)
print("CONVERSION RATES BY FIRST TYPE × TOPIC")
print("="*80)

for topic in sorted(df['topic'].unique()):
    sub = df[df['topic']==topic]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb==0 or nh==0:
        print(f"\n{topic:20s}: only {'bot' if nb>0 else 'human'} (n={nb+nh})")
        continue
    db, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{topic:20s}  Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':20s}  {db/nb*100:5.1f}%           {dh/nh*100:5.1f}%")
    if db>0: print(f"  {'Trial rate:':20s}  {tb/db*100:5.1f}%           {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':20s}  {pb/tb*100:5.1f}%           {ph/th*100:5.1f}%")

# ============ BREAKDOWN BY REGION ============
print("\n" + "="*80)
print("CONVERSION RATES BY FIRST TYPE × REGION")
print("="*80)

for region in sorted(df['region'].unique()):
    sub = df[df['region']==region]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb==0 or nh==0:
        print(f"\n{region:25s}: only {'bot' if nb>0 else 'human'} (n={nb+nh})")
        continue
    db, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{region:25s}  Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':20s}  {db/nb*100:5.1f}%           {dh/nh*100:5.1f}%")
    if db>0: print(f"  {'Trial rate:':20s}  {tb/db*100:5.1f}%           {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':20s}  {pb/tb*100:5.1f}%           {ph/th*100:5.1f}%")

# ============ BREAKDOWN BY SEGMENT ============
print("\n" + "="*80)
print("CONVERSION RATES BY FIRST TYPE × SEGMENT")
print("="*80)

for segment in sorted(df['segment'].unique()):
    sub = df[df['segment']==segment]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb==0 or nh==0:
        print(f"\n{segment:20s}: only {'bot' if nb>0 else 'human'} (n={nb+nh})")
        continue
    db, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{segment:20s}  Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':20s}  {db/nb*100:5.1f}%           {dh/nh*100:5.1f}%")
    if db>0: print(f"  {'Trial rate:':20s}  {tb/db*100:5.1f}%           {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':20s}  {pb/tb*100:5.1f}%           {ph/th*100:5.1f}%")

# ============ FIRST RESPONSE TIME ANALYSIS ============
print("\n" + "="*80)
print("FIRST RESPONSE TIME (MINUTES) BY TYPE")
print("="*80)
for g in ['bot_first','human_first']:
    sub = df[df['first_type']==g]
    rt = sub['first_response_mins'].dropna()
    print(f"  {g:12s}: mean={rt.mean():.1f} min, median={rt.median():.1f} min, n={len(rt)}")

# ============ DURATION BREAKDOWN BY INTENT ============
print("\n" + "="*80)
print("DURATION: First Response -> Demo Booked (days) BY INTENT × TYPE")
print("="*80)

df['first_response_at'] = pd.to_datetime(df['first_response_at'])
df['demo_booked_at'] = pd.to_datetime(df['demo_booked_at'])
df['dur_1'] = (df['demo_booked_at'] - df['first_response_at']).dt.total_seconds()/86400
df['dur_1'] = df['dur_1'].where(df['dur_1'] >= 0)

for intent in sorted(df['intent'].unique()):
    for g in ['bot_first','human_first']:
        sub = df[(df['intent']==intent) & (df['first_type']==g) & (df['dur_1'].notna())]
        if len(sub) > 0:
            print(f"  {intent:20s} {g:12s}: mean={sub['dur_1'].mean():.1f} d, median={sub['dur_1'].median():.1f} d, n={len(sub)}")