import json, numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sql = """
SELECT de."Disaster Event ID",
  json_extract(de."Impact Indicator", '$.population.affected') AS affected,
  json_extract(de."Impact Indicator", '$.population.displaced') AS displaced,
  json_extract(de."Impact Indicator", '$.population.injured') AS injured,
  json_extract(hr."Staffing", '$.personnel.total') AS staff_total,
  json_extract(hr."Staffing", '$.personnel.medical') AS staff_medical,
  json_extract(hr."Staffing", '$.personnel.logistics') AS staff_logistics,
  json_extract(hr."Staffing", '$.personnel.volunteers') AS volunteers,
  json_extract(hr."Staffing", '$.readiness.availability_percent') AS avail_pct,
  fin."budgetallot(USD)" AS budget,
  fin."fundsutilpct(%)" AS fundsutil,
  fin."costbene(USD)" AS costbene,
  fin."resourcegaps(USD)" AS gaps,
  hub."Utilization (%)" AS hub_util,
  hub."Inventory Accuracy (%)" AS inv_acc,
  tr."Total Transport Volume (tons)" AS transport_vol,
  tr."Daily Transport Volume (tons)" AS daily_vol,
  tr."Average Delivery Time" AS deliv_time,
  tr."Delivery Success Rate" AS deliv_success,
  tr."Number of Distribution Points" AS dist_points,
  tr."Number of Vehicles" AS vehicles,
  sup."Inventory resources" AS inv
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
"""
res = db.query(sql)
df = db.frame(res)
print(df.shape)
print(df.head(3))

# Parse inventory JSON into columns
inv_df = df['inv'].apply(json.loads)
df['generators'] = inv_df.apply(lambda d: d['power']['generators'])
df['fuel_l'] = inv_df.apply(lambda d: d['power']['fuel_liters'])
df['medical_units'] = inv_df.apply(lambda d: d['medical'])
df['shelter_units'] = inv_df.apply(lambda d: d['shelter']['units'])
df['blankets'] = inv_df.apply(lambda d: d['shelter']['blankets'])
df['food_tons'] = inv_df.apply(lambda d: d['essentials']['food_tons'])
df['water_l'] = inv_df.apply(lambda d: d['essentials']['water_liters'])
df['hygiene_kits'] = inv_df.apply(lambda d: d['hygiene_kits'])

# Ratios
df['affected_per_staff'] = df['affected']/df['staff_total']
df['affected_per_1000usd'] = df['affected']/(df['budget']/1000)
df['affected_per_food_ton'] = df['affected']/df['food_tons']
df['displaced_per_shelter'] = df['displaced']/df['shelter_units']
df['injured_per_medic'] = df['injured']/df['staff_medical']
df['affected_per_transport_ton'] = df['affected']/df['transport_vol']
df['affected_per_dist_point'] = df['affected']/df['dist_points']

# Correlations of resources with delivery success rate
targets = ['deliv_success']
feats = ['staff_total','volunteers','avail_pct','budget','fundsutil','transport_vol','daily_vol','dist_points','vehicles','hub_util','inv_acc','generators','medical_units','shelter_units','food_tons','water_l','hygiene_kits']
rows=[]
for f in feats:
    sub = df[[f,'deliv_success']].dropna()
    if sub[f].std()==0 or sub['deliv_success'].std()==0:
        continue
    r,p = stats.pearsonr(sub[f], sub['deliv_success'])
    rows.append((f, round(r,3), round(p,4), len(sub)))
corr = pd.DataFrame(rows, columns=['resource','pearson_r_with_delivery_success','p','n']).sort_values('pearson_r_with_delivery_success', key=abs, ascending=False)
print(corr.to_string(index=False))

# Correlation of fundsutil with delivery success and staffing with hub util
print("\nSpearman:")
rows=[]
for f in feats:
    sub = df[[f,'deliv_success']].dropna()
    r,p = stats.spearmanr(sub[f], sub['deliv_success'])
    rows.append((f, round(r,3), round(p,4), len(sub)))
corr2 = pd.DataFrame(rows, columns=['resource','spearman_rho','p','n']).sort_values('spearman_rho', key=abs, ascending=False)
print(corr2.head(10).to_string(index=False))

df.to_csv('/work/l5_dataset.csv', index=False)
print("saved", df.shape)