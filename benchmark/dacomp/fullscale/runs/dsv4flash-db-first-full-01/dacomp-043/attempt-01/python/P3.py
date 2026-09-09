import matplotlib.pyplot as plt
import numpy as np

# Data from SQL queries
# Deceased: n=58 records, avg_temp=38.02, min=36.0, max=39.9
# Recovered: n=224 records, avg_temp=38.70, min=36.0, max=42.1
# Let me pull actual temperature values to make a boxplot
import json, os

# Query temperature data directly via db
rows = db.query("""
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
""")

deceased_temps = []
recovered_temps = []
for r in rows:
    g = r[0]
    t = r[1]
    if g == 'Deceased':
        deceased_temps.append(t)
    else:
        recovered_temps.append(t)

print(f"Deceased temps: n={len(deceased_temps)}, mean={np.mean(deceased_temps):.2f}")
print(f"Recovered temps: n={len(recovered_temps)}, mean={np.mean(recovered_temps):.2f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax1 = axes[0]
bp = ax1.boxplot([deceased_temps, recovered_temps], labels=['Deceased (n=58)', 'Recovered (n=224)'], patch_artist=True)
bp['boxes'][0].set_facecolor('#d62728')
bp['boxes'][1].set_facecolor('#2ca02c')
ax1.set_ylabel('Highest Body Temperature (°C)')
ax1.set_title('Highest Body Temperature by Outcome')
ax1.set_ylim(35, 43)

# Data completeness
rows2 = db.query("""
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Data Completeness Score" AS score
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
""")
dec_scores = [r[1] for r in rows2 if r[0] == 'Deceased']
rec_scores = [r[1] for r in rows2 if r[0] == 'Recovered']
print(f"Deceased scores: n={len(dec_scores)}, mean={np.mean(dec_scores):.2f}")
print(f"Recovered scores: n={len(rec_scores)}, mean={np.mean(rec_scores):.2f}")

ax2 = axes[1]
bp2 = ax2.boxplot([dec_scores, rec_scores], labels=['Deceased (n=56)', 'Recovered (n=155)'], patch_artist=True)
bp2['boxes'][0].set_facecolor('#d62728')
bp2['boxes'][1].set_facecolor('#2ca02c')
ax2.set_ylabel('Data Completeness Score (0-100)')
ax2.set_title('Medical Record Data Completeness')

plt.tight_layout()
plt.savefig('/work/figure4_temperature_completeness.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 created.")