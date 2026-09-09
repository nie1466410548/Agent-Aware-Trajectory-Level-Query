import pandas as pd
from scipy import stats

df = pd.read_csv('/work/l5_dataset.csv')

# Fetch beneficiary outcome metrics and merge
sql = """
SELECT de."Disaster Event ID",
  ba."Distribution Equity Index" AS equity,
  ba."Affected Population Feedback Score" AS feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
"""
res = db.query(sql)
bdf = db.frame(res)
df = df.merge(bdf, on='Disaster Event ID', how='left')
print(df[['equity','feedback']].describe())

outcomes = ['deliv_success','equity','feedback']
res_features = ['staff_total','volunteers','budget','fundsutil','transport_vol','daily_vol','dist_points','vehicles','hub_util','inv_acc','generators','medical_units','shelter_units','food_tons','water_l','hygiene_kits','avail_pct']
rows=[]
for o in outcomes:
    for f in res_features:
        sub = df[[f,o]].dropna()
        if len(sub)<30: continue
        r,p = stats.pearsonr(sub[f], sub[o])
        rows.append((o,f,round(r,3),round(p,4)))
c = pd.DataFrame(rows, columns=['outcome','resource','r','p'])
sig = c[c['p']<0.05]
print("\nSignificant correlations (p<0.05):")
print(sig.to_string(index=False))
if len(sig)==0:
    print("None - all resource-outcome correlations for Level 5 are non-significant")

# Compare equity/feedback for Level 5 vs non-Level 5
sql2 = """
SELECT de."Disaster Severity Level",
  ROUND(AVG(ba."Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG(ba."Affected Population Feedback Score"),2) AS avg_feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
GROUP BY de."Disaster Severity Level"
ORDER BY de."Disaster Severity Level"
"""
res2 = db.query(sql2)
print(db.frame(res2).to_string(index=False))