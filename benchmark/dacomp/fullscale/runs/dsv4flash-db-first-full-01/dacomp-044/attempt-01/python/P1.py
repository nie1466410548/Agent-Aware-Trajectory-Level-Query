
import pandas as pd, numpy as np
from scipy import stats

df = db.frame(db.query("""
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty
FROM health_education
WHERE "Population Covered" = 'Student'
"""))

df['behav_sig'] = (df['behav']=='Significant').astype(int)
df['track_sig'] = (df['track']=='Significant').astype(int)
df['eff_sig'] = (df['eff']=='Significant').astype(int)
df['both_sig'] = ((df['behav']=='Significant') & (df['track']=='Significant')).astype(int)
df['behav_or_track'] = ((df['behav']=='Significant') | (df['track']=='Significant')).astype(int)

print("Total student campaigns:", len(df))
print(df[['format','location','behav','track','eff']].groupby(['format','location']).size().unstack(fill_value=0))
print()

def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan, np.nan)
    p = k/n
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n))/denom
    half = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/denom
    return p, max(0,centre-half), min(1,centre+half)

rows = []
for (fmt, loc), g in df.groupby(['format','location']):
    n = len(g)
    b = g.behav_sig.sum(); t = g.track_sig.sum(); bo = g.both_sig.sum(); e = g.eff_sig.sum()
    pb, lb, ub = wilson(b, n)
    rows.append({'format':fmt,'location':loc,'n':n,
                 'behav_sig':b,'behav_pct':100*b/n,
                 'track_sig':t,'track_pct':100*t/n,
                 'both_sig':bo,'both_pct':100*bo/n,
                 'eff_sig':e,'eff_pct':100*e/n,
                 'both_ci_low':lb,'both_ci_high':ub})
res = pd.DataFrame(rows).sort_values(['both_pct','n'], ascending=[False,False])
print(res.round(1).to_string(index=False))
print()

# Overall student totals
print("Overall students: behav sig =", df.behav_sig.sum(), "/", len(df),
      f"({100*df.behav_sig.mean():.1f}%), track sig =", df.track_sig.sum(),
      f"({100*df.track_sig.mean():.1f}%), both =", df.both_sig.sum(), f"({100*df.both_sig.mean():.1f}%)")

# Chi-square tests of independence
ct_b = pd.crosstab(df['format'], df['behav_sig'])
ct_t = pd.crosstab(df['format'], df['track_sig'])
ct_lb = pd.crosstab(df['location'], df['behav_sig'])
ct_lt = pd.crosstab(df['location'], df['track_sig'])
for name, ct in [('format x behav', ct_b), ('format x track', ct_t), ('location x behav', ct_lb), ('location x track', ct_lt)]:
    chi2, p, dof, exp = stats.chi2_contingency(ct)
    print(f"{name}: chi2={chi2:.3f}, p={p:.3f}, dof={dof}, min_exp={exp.min():.1f}")
