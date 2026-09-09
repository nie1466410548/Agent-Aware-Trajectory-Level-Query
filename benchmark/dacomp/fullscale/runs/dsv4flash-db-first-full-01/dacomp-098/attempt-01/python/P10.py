import pandas as pd
import numpy as np
import json

df = pd.read_csv('/work/contact_funnel.csv')

# Load company info
result = db.query("""
SELECT ct.contact_id, ct.all_contact_company_names AS company_name,
       c.company_id, c.industry, c.plan_name, c.plan_id, c.monthly_spend
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
""")
comp = db.frame(result)
comp = comp.drop_duplicates(subset='contact_id')
print(f"Contact-company mapping: {len(comp)} contacts, matched companies: {comp['industry'].notna().sum()}")

df2 = df.merge(comp, on='contact_id', how='left')
df2.to_csv('/work/contact_funnel_company.csv', index=False)

print("\nTop company names in data:")
print(df2['company_name'].value_counts().head(10))

print("\nIndustry distribution:")
print(df2['industry'].value_counts(dropna=False).head(15))

print("\nPlan distribution:")
print(df2['plan_name'].value_counts(dropna=False).head(10))

# ============ Conversion by industry × type ============
print("\n" + "="*80)
print("CONVERSION RATES BY INDUSTRY × FIRST TYPE")
print("="*80)
for industry in df2['industry'].dropna().unique():
    sub = df2[df2['industry']==industry]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb < 5 or nh < 5:
        continue
    db_, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{industry:25s} Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':18s} {db_/nb*100:5.1f}%       {dh/nh*100:5.1f}%")
    if db_>0: print(f"  {'Trial rate:':18s} {tb/db_*100:5.1f}%       {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':18s} {pb/tb*100:5.1f}%       {ph/th*100:5.1f}%")

# ============ Conversion by plan × type ============
print("\n" + "="*80)
print("CONVERSION RATES BY PLAN × FIRST TYPE")
print("="*80)
for plan in df2['plan_name'].dropna().unique():
    sub = df2[df2['plan_name']==plan]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb < 5 or nh < 5:
        continue
    db_, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{plan:15s} Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':18s} {db_/nb*100:5.1f}%       {dh/nh*100:5.1f}%")
    if db_>0: print(f"  {'Trial rate:':18s} {tb/db_*100:5.1f}%       {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':18s} {pb/tb*100:5.1f}%       {ph/th*100:5.1f}%")