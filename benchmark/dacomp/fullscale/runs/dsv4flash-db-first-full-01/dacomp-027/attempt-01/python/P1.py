import pandas as pd, numpy as np
from scipy import stats

q = """
SELECT d."Disaster Event ID", d."Disaster Level", d."Disaster Type",
       c."Secincident Count",
       json_extract(d."Impact Indicator",'$.population.affected') AS affected,
       json_extract(d."Impact Indicator",'$.population.displaced') AS displaced,
       json_extract(d."Impact Indicator",'$.population.injured') AS injured,
       json_extract(d."Impact Indicator",'$.population.casualties') AS casualties,
       json_extract(d."Impact Indicator",'$.population.missing') AS missing,
       json_extract(d."Impact Indicator",'$.infrastructure.damage_percent') AS damage_pct,
       json_extract(d."Impact Indicator",'$.infrastructure.power_outage_percent') AS power_pct,
       json_extract(d."Impact Indicator",'$.infrastructure.water_damage_percent') AS water_pct,
       e."Environmental Impact Rate", e."Waste Management Status", e."Recycling Rate (%)" AS recycling,
       e."Carbon Emissions (tons)" AS carbon, e."Renewable Energy Share (%)" AS renewable,
       e."Water Quality Index" AS wqi, e."Sanitation Coverage Rate" AS sanitation,
       e."Disease Risk", e."Medical Emergency Response Capacity" AS med_cap,
       e."Vaccination Coverage Rate" AS vaccination, e."Mental Health Assistance" AS mental,
       o."Estimated Duration (days)" AS duration, o."Response Phase", o."Operation Status",
       f."fundsutilpct(%)" AS fund_util, f."resourcegaps(USD)" AS resource_gap,
       t."Delivery Success Rate" AS delivery, t."Average Delivery Time" AS deliv_time,
       c."stakeholdersatisf" AS stk_sat, c."publicperception" AS pub_perm,
       c."reportcompliance" AS report_comp
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"
"""
res = db.query(q)
df = db.frame(res)
print(df.shape)
print(df.dtypes.value_counts())
print(df.isna().sum().sum())
df.to_csv('/work/full_joined.csv', index=False)
print(df.head(3))
