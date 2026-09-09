import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/full_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low(0-32)','Med(33-65)','High(66-100)'])

# Pull coordination and operational categoricals
q = """
SELECT c."Secincident Count", c."Safety Ranking", c."Accesslimitation", c."coordeffectlvl",
       c."infosharingstate", c."monitoringfreq", c."evaluationstage", c."lessonslearnedstage",
       c."contingencyplanstage", c."riskmitigationsteps", c."insurancescope", c."compliancestate",
       c."auditstate", c."qualitycontrolsteps", c."mediacoversentiment", c."documentationstate",
       o."Response Phase", o."Operation Status", o."Emergency Level", o."Priority", o."Resource Allocation Status", o."Supply Flow Status",
       d."Disaster Level", d."Disaster Type"
FROM coordination_and_evaluation c
JOIN operations1 o ON o."Disaster Reference ID"=c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID"=c."Distribution Reference ID"
"""
res = db.query(q)
cat_df = db.frame(res)
cat_df['sec_group'] = pd.cut(cat_df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low(0-32)','Med(33-65)','High(66-100)'])
print(cat_df.shape)
cat_df.to_csv('/work/cat_joined.csv', index=False)

cat_cols = ['Safety Ranking','Accesslimitation','coordeffectlvl','infosharingstate','monitoringfreq',
            'evaluationstage','lessonslearnedstage','contingencyplanstage','riskmitigationsteps','insurancescope',
            'compliancestate','auditstate','qualitycontrolsteps','mediacoversentiment','documentationstate',
            'Response Phase','Operation Status','Emergency Level','Priority','Resource Allocation Status','Supply Flow Status']
print("\n=== Chi-square: sec_group vs categorical ===")
for col in cat_cols:
    ct = pd.crosstab(cat_df['sec_group'], cat_df[col])
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    flag = '***' if p<0.05 else ''
    if p < 0.15:
        print(f"{col}: chi2={chi2:.2f}, p={p:.4f} {flag}")
        print(ct)

# Disease Risk proportion by sec group (from main df)
print("\n=== Disease Risk proportion by sec_group ===")
print(pd.crosstab(df['sec_group'], df['Disease Risk'], normalize='index').round(3))

# Disease risk by disaster level
print("\n=== Disease Risk proportion by Disaster Level ===")
print(pd.crosstab(df['Disaster Level'], df['Disease Risk'], normalize='index').round(3))

# Environmental Impact Rate proportion by disaster level
print("\n=== Environmental Impact Rate proportion by Disaster Level ===")
print(pd.crosstab(df['Disaster Level'], df['Environmental Impact Rate'], normalize='index').round(3))

# Combined: within high disease risk, what is medical capacity / vaccination by sec group?
print("\n=== Among HIGH Disease Risk events: medical capacity by sec_group ===")
sub = df[df['Disease Risk']=='High']
print(pd.crosstab(sub['sec_group'], sub['med_cap'], normalize='index').round(3))
print("\nVaccination coverage by Disease Risk and sec_group:")
print(sub.groupby('sec_group')['vaccination'].agg(['count','mean','median']).round(1))