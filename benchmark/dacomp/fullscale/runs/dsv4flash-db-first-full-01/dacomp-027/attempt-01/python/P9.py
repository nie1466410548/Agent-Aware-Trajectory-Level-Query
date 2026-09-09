import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/full_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])

# Access limitation by sec_group
res = db.query("""
SELECT c."Secincident Count", c."Accesslimitation", c."Safety Ranking",
       e."Disease Risk", e."Water Quality Index", e."Vaccination Coverage Rate",
       e."Sanitation Coverage Rate", e."Mental Health Assistance",
       d."Disaster Level"
FROM coordination_and_evaluation c
JOIN environment_and_health e ON e."Disaster Reference ID" = c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID" = c."Distribution Reference ID"
""")
acc = db.frame(res)
acc['sec_group'] = pd.cut(acc['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])

# Access limitation and disease risk
print("=== Access Limitation × Disease Risk (sec_group) ===")
print(pd.crosstab([acc['sec_group'], acc['Accesslimitation']], acc['Disease Risk']))

# Among severe access limitation, disease risk by sec
print("\n=== Among Severe Access: Disease Risk by sec_group ===")
sub_severe = acc[acc['Accesslimitation']=='Severe']
print(pd.crosstab(sub_severe['sec_group'], sub_severe['Disease Risk'], normalize='index').round(3))

# WQI and vaccination by access × sec
print("\n=== WQI by Access Limitation and sec_group ===")
print(acc.groupby(['Accesslimitation','sec_group'])['Water Quality Index'].agg(['mean','median']).round(1))
print("\n=== Vaccination by Access Limitation and sec_group ===")
print(acc.groupby(['Accesslimitation','sec_group'])['Vaccination Coverage Rate'].agg(['mean','median']).round(1))

# Mental health by access × sec
print("\n=== Mental Health Assistance by Access Limitation × sec_group ===")
print(pd.crosstab([acc['Accesslimitation'], acc['sec_group']], acc['Mental Health Assistance'], normalize='index').round(3))

# Check: Among HIGH disease risk, proportion with Limited mental health by sec group
print("\n=== Among High Disease Risk: Mental Health by sec_group ===")
sub_high = acc[acc['Disease Risk']=='High']
print(pd.crosstab(sub_high['sec_group'], sub_high['Mental Health Assistance'], normalize='index').round(3))