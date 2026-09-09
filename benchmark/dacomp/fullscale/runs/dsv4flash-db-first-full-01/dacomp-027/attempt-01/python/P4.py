import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/full_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low(0-32)','Med(33-65)','High(66-100)'])
df['level_num'] = df['Disaster Level'].str.extract('(\d)').astype(int)

# T-test: vaccination high vs low sec groups
hi = df[df['sec_group']=='High(66-100)']
lo = df[df['sec_group']=='Low(0-32)']
for col in ['vaccination','wqi','sanitation','carbon','recycling','delivery','stk_sat','pub_perm']:
    t, p = stats.ttest_ind(hi[col], lo[col], equal_var=False)
    print(f"{col}: High vs Low t={t:.3f}, p={p:.4f}, means Hi={hi[col].mean():.1f} Lo={lo[col].mean():.1f}")

# Vaccination among HIGH disease risk, high vs low sec
sub_hi_risk = df[df['Disease Risk']=='High']
h = sub_hi_risk[sub_hi_risk['sec_group']=='High(66-100)']['vaccination']
l = sub_hi_risk[sub_hi_risk['sec_group']=='Low(0-32)']['vaccination']
t,p = stats.ttest_ind(h,l,equal_var=False)
print(f"\nAmong High-disease-risk: vaccination High-sec vs Low-sec: t={t:.3f}, p={p:.4f}; mean Hi={h.mean():.1f}, Lo={l.mean():.1f}")

# Interaction: high sec + disaster level -> disease risk proportion
print("\n=== Disease Risk High proportion by (level, sec_group) ===")
ct = pd.crosstab([df['Disaster Level'], df['sec_group']], df['Disease Risk'], normalize='index').round(3)
print(ct)

# Environmental impact High proportion by (level, sec_group)
print("\n=== Env Impact High proportion by (level, sec_group) ===")
ct2 = pd.crosstab([df['Disaster Level'], df['sec_group']], df['Environmental Impact Rate'], normalize='index').round(3)
print(ct2)

# WQI / Vaccination means by level and sec group
print("\n=== Vaccination by level & sec_group (mean) ===")
print(df.pivot_table(index='Disaster Level', columns='sec_group', values='vaccination', aggfunc='mean').round(1))
print("\n=== WQI by level & sec_group (mean) ===")
print(df.pivot_table(index='Disaster Level', columns='sec_group', values='wqi', aggfunc='mean').round(1))

# Interaction test: 2-way ANOVA impossible w/o statsmodels; use group means of composite
# Composite "people impact" = casualties+injured+missing+displaced per affected
df['people_impact_rate'] = (df['casualties']+df['injured']+df['missing']+df['displaced'])/(df['affected']+1)

# Check if disease risk relates to env indicators
print("\n=== Env indicators by Disease Risk ===")
print(df.groupby('Disease Risk')[['wqi','sanitation','carbon','vaccination','renewable']].agg(['mean','median']).round(1))

# Response phase / operation status by level
print("\n=== Operation Status by Disaster Level ===")
print(pd.crosstab(df['Disaster Level'], df['Operation Status'], normalize='index').round(3))
print("\n=== Response Phase by Disaster Level ===")
print(pd.crosstab(df['Disaster Level'], df['Response Phase'], normalize='index').round(3))