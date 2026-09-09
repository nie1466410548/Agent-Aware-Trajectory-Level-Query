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
       "Knowledge Assessment" AS knowledge,
       "New Media Metrics (Views/Shares)" AS new_media
FROM health_education
WHERE "Population Covered" = 'Student'
"""))

df['both_sig'] = ((df['behav']=='Significant') & (df['track']=='Significant')).astype(int)

# Parse awareness rate and knowledge assessment
def parse_pct(val):
    if pd.isna(val) or val is None: return np.nan
    if isinstance(val, str):
        val = val.replace('%','').strip()
        try: return float(val)
        except: return np.nan
    return np.nan

df['awareness_rate'] = df['awareness'].apply(parse_pct)
df['knowledge_rate'] = df['knowledge'].apply(parse_pct)

# Parse new media views
def parse_views(val):
    if pd.isna(val) or val is None: return np.nan
    if isinstance(val, str) and '/' in val:
        try: return float(val.split('/')[0].strip())
        except: return np.nan
    return np.nan

df['views'] = df['new_media'].apply(parse_views)

print("Comparison of campaigns with both_sig vs not:")
print("="*80)
for metric, label in [('awareness_rate','Awareness Rate (%)'),
                      ('knowledge_rate','Knowledge Assessment (%)'),
                      ('views','New Media Views'),
                      ('freq','Campaign Frequency (times/month)'),
                      ('qty','Distribution Quantity')]:
    both = df[df['both_sig']==1][metric].dropna()
    not_both = df[df['both_sig']==0][metric].dropna()
    print(f"\n{label}:")
    print(f"  Both Significant (n={len(both)}): mean={both.mean():.1f}, median={both.median():.1f}")
    print(f"  Others (n={len(not_both)}): mean={not_both.mean():.1f}, median={not_both.median():.1f}")
    if len(both) > 2 and len(not_both) > 2:
        t, p = stats.ttest_ind(both, not_both, equal_var=False)
        print(f"  Welch t-test: t={t:.3f}, p={p:.3f}")

# Check content distribution
print("\n\nContent distribution for both_sig campaigns:")
print(df[df['both_sig']==1]['content'].value_counts())

print("\nContent distribution for all student campaigns:")
print(df['content'].value_counts())

# Format × Location breakdown for both_sig
print("\n\nFormat × Location × Content for both_sig:")
print(df[df['both_sig']==1][['format','location','content']].value_counts().to_string())

# Compare with non-student populations
ns = db.frame(db.query("""
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Population Covered" AS pop,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track
FROM health_education
WHERE "Population Covered" != 'Student'
"""))
ns['both_sig'] = ((ns['behav']=='Significant') & (ns['track']=='Significant')).astype(int)

print("\n\nNon-student campaigns: both_sig rate =", 
      f"{100*ns.both_sig.mean():.1f}% ({ns.both_sig.sum()}/{len(ns)})")
print(f"Student campaigns: both_sig rate = {100*df.both_sig.mean():.1f}% ({df.both_sig.sum()}/{len(df)})")
chi2, p = stats.chi2_contingency(pd.crosstab(
    pd.concat([df.assign(pop='Student'), ns.assign(pop='Non-student')])['pop'],
    pd.concat([df['both_sig'], ns['both_sig']])
))[:2]
print(f"Chi-square test: chi2={chi2:.3f}, p={p:.3f}")

# Grouped analysis for students
print("\n\n=== Student Campaign Analysis Summary ===")
print(f"Total student campaigns: {len(df)}")
print(f"Campaigns with both significant behavioral change + tracking: {df.both_sig.sum()} ({100*df.both_sig.mean():.1f}%)")
print(f"Campaigns with significant behavioral change: {df[df['behav']=='Significant'].shape[0]} ({100*(df['behav']=='Significant').mean():.1f}%)")
print(f"Campaigns with significant tracking: {df[df['track']=='Significant'].shape[0]} ({100*(df['track']=='Significant').mean():.1f}%)")