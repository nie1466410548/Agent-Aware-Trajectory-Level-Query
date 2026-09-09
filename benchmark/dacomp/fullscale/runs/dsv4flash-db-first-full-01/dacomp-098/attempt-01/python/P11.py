import pandas as pd
import numpy as np
from scipy import stats

df2 = pd.read_csv('/work/contact_funnel_company.csv')

# Parse lead source from contact tags
result = db.query("""
SELECT contact_id, all_contact_tags,
  CASE WHEN instr(all_contact_tags,'source:')>0 THEN
    substr(all_contact_tags, instr(all_contact_tags,'source:')+7,
      CASE WHEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')>0
        THEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')-1
        ELSE length(substr(all_contact_tags,instr(all_contact_tags,'source:')+7)) END)
  END AS lead_source
FROM intercom__contact_enhanced
""")
src = db.frame(result)
df3 = df2.merge(src[['contact_id','lead_source']], on='contact_id', how='left')
df3.to_csv('/work/contact_funnel_full.csv', index=False)

print("Lead source distribution:")
print(df3['lead_source'].value_counts(dropna=False))

# ============ Conversion by lead source × type ============
print("\n" + "="*80)
print("CONVERSION RATES BY LEAD SOURCE × FIRST TYPE")
print("="*80)
for source in df3['lead_source'].dropna().unique():
    sub = df3[df3['lead_source']==source]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    if nb < 5 or nh < 5:
        continue
    db_, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{source:15s} Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':18s} {db_/nb*100:5.1f}%       {dh/nh*100:5.1f}%")
    if db_>0: print(f"  {'Trial rate:':18s} {tb/db_*100:5.1f}%       {th/dh*100:5.1f}%")
    if tb>0: print(f"  {'Paid rate:':18s} {pb/tb*100:5.1f}%       {ph/th*100:5.1f}%")

# ============ Independent Consultant (unmatched) group ============
print("\n" + "="*80)
print("UNMATCHED ('Independent Consultant') vs MATCHED COMPANIES")
print("="*80)
df3['grp'] = np.where(df3['industry'].isna(), 'unmatched', 'matched')
for grp in ['unmatched','matched']:
    sub = df3[df3['grp']==grp]
    bot = sub[sub['first_type']=='bot_first']
    human = sub[sub['first_type']=='human_first']
    nb, nh = len(bot), len(human)
    db_, tb, pb = bot['reached_demo'].sum(), bot['reached_trial'].sum(), bot['reached_paid'].sum()
    dh, th, ph = human['reached_demo'].sum(), human['reached_trial'].sum(), human['reached_paid'].sum()
    print(f"\n{grp:12s} Bot(n={nb})  Human(n={nh})")
    print(f"  {'Demo rate:':18s} {db_/nb*100:5.1f}%       {dh/nh*100:5.1f}%")
    print(f"  {'Trial rate:':18s} {tb/db_*100:5.1f}%       {th/dh*100:5.1f}%")
    print(f"  {'Paid rate:':18s} {pb/tb*100:5.1f}%       {ph/th*100:5.1f}%")

# ============ Significance tests on key differences ============
print("\n" + "="*80)
print("SIGNIFICANCE TESTS ON KEY INDUSTRY DIFFERENCES")
print("="*80)

def chi2_cols(sub, col):
    b = sub[sub['first_type']=='bot_first']
    h = sub[sub['first_type']=='human_first']
    table = np.array([[b[col].sum(), len(b)-b[col].sum()],
                      [h[col].sum(), len(h)-h[col].sum()]])
    chi2, p, _, _ = stats.chi2_contingency(table)
    return chi2, p

for industry in ['E-commerce','Media & Entertainment','Manufacturing','SaaS','Travel']:
    sub = df3[df3['industry']==industry]
    if len(sub) < 20: continue
    b = sub[sub['first_type']=='bot_first']
    h = sub[sub['first_type']=='human_first']
    print(f"\n{industry}:")
    for col, name in [('reached_demo','Demo'),('reached_paid','Paid')]:
        # Use conditional where appropriate
        if col=='reached_demo':
            chi2, p = chi2_cols(sub, col)
            print(f"  {name}: bot={b[col].mean()*100:.1f}% human={h[col].mean()*100:.1f}% p={p:.3f}")
        else:
            # paid among trial
            bt = b[b['reached_trial']==1]; ht = h[h['reached_trial']==1]
            if len(bt)>4 and len(ht)>4:
                table = np.array([[bt['reached_paid'].sum(), len(bt)-bt['reached_paid'].sum()],
                                  [ht['reached_paid'].sum(), len(ht)-ht['reached_paid'].sum()]])
                chi2, p, _, _ = stats.chi2_contingency(table)
                print(f"  {name}|trial: bot={bt['reached_paid'].mean()*100:.1f}% human={ht['reached_paid'].mean()*100:.1f}% p={p:.3f}")

# Lead source significance
print("\n" + "="*80)
print("SIGNIFICANCE TESTS BY LEAD SOURCE")
print("="*80)
for source in df3['lead_source'].dropna().unique():
    sub = df3[df3['lead_source']==source]
    b = sub[sub['first_type']=='bot_first']
    h = sub[sub['first_type']=='human_first']
    if len(b)<10 or len(h)<10: continue
    for col, name in [('reached_demo','Demo'),('reached_paid','Paid')]:
        if col=='reached_demo':
            chi2, p = chi2_cols(sub, col)
        else:
            bt = b[b['reached_trial']==1]; ht = h[h['reached_trial']==1]
            if len(bt)<5 or len(ht)<5: continue
            table = np.array([[bt['reached_paid'].sum(), len(bt)-bt['reached_paid'].sum()],
                              [ht['reached_paid'].sum(), len(ht)-ht['reached_paid'].sum()]])
            chi2, p, _, _ = stats.chi2_contingency(table)
        print(f"  {source:15s} {name:10s}: bot={b[col].mean()*100 if col=='reached_demo' else bt['reached_paid'].mean()*100:.1f}% human={h[col].mean()*100 if col=='reached_demo' else ht['reached_paid'].mean()*100:.1f}% p={p:.3f}")