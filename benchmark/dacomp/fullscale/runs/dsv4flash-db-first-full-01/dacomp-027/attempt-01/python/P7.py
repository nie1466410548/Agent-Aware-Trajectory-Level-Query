import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/full_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
df['level_num'] = df['Disaster Level'].str.extract('(\d)').astype(int)

# Get damage_level from JSON
res = db.query("""SELECT "Disaster Event ID",
 json_extract("Impact Indicator",'$.damage_level') AS damage_level,
 json_extract("Impact Indicator",'$.communication') AS communication,
 json_extract("Impact Indicator",'$.transportation') AS transportation
FROM disaster_events""")
dl = db.frame(res)
df2 = df.merge(dl, on='Disaster Event ID')

print("=== Damage Level by sec_group (normalized) ===")
ct = pd.crosstab(df2['sec_group'], df2['damage_level'], normalize='index').round(3)
print(ct)
chi2, p, _, _ = stats.chi2_contingency(pd.crosstab(df2['sec_group'], df2['damage_level']))
print(f"Chi2={chi2:.2f}, p={p:.4f}")

print("\n=== Damage Level by Disaster Level (normalized) ===")
ct2 = pd.crosstab(df2['Disaster Level'], df2['damage_level'], normalize='index').round(3)
print(ct2)
chi2b, pb, _, _ = stats.chi2_contingency(pd.crosstab(df2['Disaster Level'], df2['damage_level']))
print(f"Chi2={chi2b:.2f}, p={pb:.4f}")

print("\n=== Communication by sec_group ===")
ct3 = pd.crosstab(df2['sec_group'], df2['communication'], normalize='index').round(3)
print(ct3)
chi2c, pc, _, _ = stats.chi2_contingency(pd.crosstab(df2['sec_group'], df2['communication']))
print(f"Chi2={chi2c:.2f}, p={pc:.4f}")

print("\n=== Transportation by sec_group ===")
ct4 = pd.crosstab(df2['sec_group'], df2['transportation'], normalize='index').round(3)
print(ct4)
chi2d, pd_, _, _ = stats.chi2_contingency(pd.crosstab(df2['sec_group'], df2['transportation']))
print(f"Chi2={chi2d:.2f}, p={pd_:.4f}")

# Cramer's V for disease risk vs sec group
def cramers_v(ct):
    chi2 = stats.chi2_contingency(ct)[0]
    n = ct.values.sum()
    r, k = ct.shape
    return np.sqrt(chi2 / (n * min(k-1, r-1)))

ct_risk = pd.crosstab(df['sec_group'], df['Disease Risk'])
print(f"\nCramer's V (Disease Risk vs sec_group): {cramers_v(ct_risk):.3f}")

# Interaction: High disease risk proportion by (sec group, level)
print("\n=== High Disease Risk proportion by level & sec_group ===")
piv = df.pivot_table(index='Disaster Level', columns='sec_group', values='Disease Risk',
                     aggfunc=lambda x: (x=='High').mean()).round(3)
print(piv)

# High Environmental impact proportion by level & sec_group
print("\n=== High Env Impact proportion by level & sec_group ===")
piv2 = df.pivot_table(index='Disaster Level', columns='sec_group', values='Environmental Impact Rate',
                      aggfunc=lambda x: (x=='High').mean()).round(3)
print(piv2)

# Active operations proportion by level
print("\n=== Active Operation proportion by level ===")
print(df.pivot_table(index='Disaster Level', values='Operation Status', aggfunc=lambda x: (x=='Active').mean()).round(3))

# Completed operation proportion by level
print("\n=== Completed Operation proportion by level ===")
print(df.pivot_table(index='Disaster Level', values='Operation Status', aggfunc=lambda x: (x=='Completed').mean()).round(3))

# Sustained: estimated duration by level
print("\n=== Duration by level ===")
print(df.groupby('Disaster Level')['duration'].agg(['mean','median']).round(1))