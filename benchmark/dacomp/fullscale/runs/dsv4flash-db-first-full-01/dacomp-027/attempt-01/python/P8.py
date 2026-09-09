import pandas as pd, numpy as np
from scipy import stats

# Funding state by sec_group
res = db.query("""
SELECT f."Disaster Reference ID", f."fundingstate", f."costbene(USD)", f."budgetallot(USD)", f."donorcommitments(USD)",
       c."Secincident Count"
FROM financials1 f
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = f."Disaster Reference ID"
""")
fin = db.frame(res)
fin['sec_group'] = pd.cut(fin['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])

print("=== Funding State by sec_group ===")
ct = pd.crosstab(fin['sec_group'], fin['fundingstate'])
chi2, p, _, _ = stats.chi2_contingency(ct)
print(f"Chi2={chi2:.2f}, p={p:.4f}")
print(ct)

print("\n=== Financial means by sec_group ===")
print(fin.groupby('sec_group')[['costbene(USD)','budgetallot(USD)','donorcommitments(USD)']].mean().round(0))

# Also check Safety Ranking by sec group
res2 = db.query("""
SELECT c."Secincident Count", c."Safety Ranking", c."Accesslimitation", c."coordeffectlvl"
FROM coordination_and_evaluation c
""")
safe = db.frame(res2)
safe['sec_group'] = pd.cut(safe['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])

print("\n=== Safety Ranking by sec_group ===")
ct2 = pd.crosstab(safe['sec_group'], safe['Safety Ranking'])
chi2_2, p_2, _, _ = stats.chi2_contingency(ct2)
print(f"Chi2={chi2_2:.2f}, p={p_2:.4f}")
print(ct2)

print("\n=== Access Limitation by sec_group ===")
ct3 = pd.crosstab(safe['sec_group'], safe['Accesslimitation'])
chi2_3, p_3, _, _ = stats.chi2_contingency(ct3)
print(f"Chi2={chi2_3:.2f}, p={p_3:.4f}")
print(ct3)

print("\n=== Coordination Effectiveness by sec_group ===")
ct4 = pd.crosstab(safe['sec_group'], safe['coordeffectlvl'])
chi2_4, p_4, _, _ = stats.chi2_contingency(ct4)
print(f"Chi2={chi2_4:.2f}, p={p_4:.4f}")
print(ct4)

# Final check: number of partner organizations by sec group
print("\n=== Partner orgs by sec_group ===")
res5 = db.query("""
SELECT c."Secincident Count", c."partnerorgs", c."dataqualityvalue", c."lessonsrecorded", c."bestpracticeslisted", c."improvementrecs"
FROM coordination_and_evaluation c
""")
part = db.frame(res5)
part['sec_group'] = pd.cut(part['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
print(part.groupby('sec_group')[['partnerorgs','dataqualityvalue','lessonsrecorded','bestpracticeslisted','improvementrecs']].mean().round(1))

# Also check JSON infrastructure damage by Disaster Level
print("\n=== Infrastructure damage by Disaster Level ===")
res6 = db.query("""
SELECT "Disaster Level",
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.damage_percent')),2) AS avg_damage_pct,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.power_outage_percent')),2) AS avg_power_outage,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.water_damage_percent')),2) AS avg_water_damage
FROM disaster_events GROUP BY "Disaster Level"
""")
print(db.frame(res6).to_string(index=False))