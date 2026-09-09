import pandas as pd, numpy as np
from scipy import stats

df = db.frame(db.query("""
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge
FROM health_education
WHERE "Population Covered" = 'Student'
"""))

# Binary columns
df['behav_sig'] = (df['behav']=='Significant').astype(int)
df['track_sig'] = (df['track']=='Significant').astype(int)
df['eff_sig'] = (df['eff']=='Significant').astype(int)

# Two interpretations:
# Interpretation 1: Long-term = eff_sig, Behavioral = behav_sig
df['int1'] = ((df['eff_sig']==1) & (df['behav_sig']==1)).astype(int)
# Interpretation 2: Long-term = track_sig, Behavioral = behav_sig
df['int2'] = ((df['track_sig']==1) & (df['behav_sig']==1)).astype(int)

print("=== Correlation between effectiveness metrics ===")
print(df[['eff_sig','track_sig','behav_sig']].corr().round(3))

print("\n=== Interpretation 1: Effectiveness Assessment (Significant) + Behavioral Change (Significant) ===")
print(f"Total: {df.int1.sum()}/{len(df)} ({100*df.int1.mean():.1f}%)")

ct1 = df.groupby(['format','location']).agg(
    n=('int1','size'),
    both_sig=('int1','sum')
).reset_index()
ct1['pct'] = (100*ct1['both_sig']/ct1['n']).round(1)
ct1 = ct1.sort_values(['pct','n'], ascending=[False,False])
print(ct1.to_string(index=False))

print("\n=== Interpretation 2: Effectiveness Tracking (Significant) + Behavioral Change (Significant) ===")
print(f"Total: {df.int2.sum()}/{len(df)} ({100*df.int2.mean():.1f}%)")

ct2 = df.groupby(['format','location']).agg(
    n=('int2','size'),
    both_sig=('int2','sum')
).reset_index()
ct2['pct'] = (100*ct2['both_sig']/ct2['n']).round(1)
ct2 = ct2.sort_values(['pct','n'], ascending=[False,False])
print(ct2.to_string(index=False))

# Treatment content preference for both interpretations
print("\n=== Content preference for Interpretation 1 (eff_sig + behav_sig) ===")
print(df[df['int1']==1]['content'].value_counts())
print("\n=== Content preference for Interpretation 2 (track_sig + behav_sig) ===")
print(df[df['int2']==1]['content'].value_counts())

# Let's create a composite capability score
# For each format × location, compute:
# 1. Rate of eff_sig (or track_sig)
# 2. Rate of behav_sig
# 3. Combined score

print("\n\n=== Comprehensive ranking (all metrics) ===")
comp = df.groupby(['format','location']).agg(
    n=('format','size'),
    behav_pct=('behav_sig', lambda x: round(100*x.mean(),1)),
    eff_pct=('eff_sig', lambda x: round(100*x.mean(),1)),
    track_pct=('track_sig', lambda x: round(100*x.mean(),1)),
    int1_pct=('int1', lambda x: round(100*x.mean(),1)),
    int2_pct=('int2', lambda x: round(100*x.mean(),1))
).reset_index()
comp['capability_score'] = (comp['behav_pct'] + comp['eff_pct'] + comp['track_pct']) / 3
comp = comp.sort_values('capability_score', ascending=False)
print(comp.round(1).to_string(index=False))

# Content analysis for the best performing combos
print("\n\n=== Content distribution for top student combos ===")
for (fmt, loc), g in df.groupby(['format','location']):
    both = g[(g['eff_sig']==1) & (g['behav_sig']==1)]
    if len(both) > 0:
        print(f"\n{fmt} @ {loc} (n={len(g)}, both_sig={len(both)}):")
        print(f"  Content: {g['content'].value_counts().to_dict()}")
        print(f"  Both sig content: {both['content'].value_counts().to_dict()}")
        print(f"  Avg freq: {g['freq'].mean():.1f}, Avg qty: {g['qty'].mean():.0f}")