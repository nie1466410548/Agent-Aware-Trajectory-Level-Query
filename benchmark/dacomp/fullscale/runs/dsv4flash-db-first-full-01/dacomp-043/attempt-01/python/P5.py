import matplotlib.pyplot as plt
import numpy as np

df_t = db.frame(db.query("""
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
"""))

df_c = db.frame(db.query("""
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Data Completeness Score" AS score
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
"""))

deceased_temps = df_t[df_t['grp']=='Deceased']['temp'].astype(float).values
recovered_temps = df_t[df_t['grp']=='Recovered']['temp'].astype(float).values
dec_scores = df_c[df_c['grp']=='Deceased']['score'].astype(float).values
rec_scores = df_c[df_c['grp']=='Recovered']['score'].astype(float).values

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax1 = axes[0]
bp = ax1.boxplot([deceased_temps, recovered_temps], labels=['Deceased (n=58)', 'Recovered (n=224)'], patch_artist=True)
bp['boxes'][0].set_facecolor('#d62728')
bp['boxes'][1].set_facecolor('#2ca02c')
ax1.set_ylabel('Highest Body Temperature (°C)')
ax1.set_title('Highest Body Temperature by Outcome')
ax1.set_ylim(35, 43)

ax2 = axes[1]
bp2 = ax2.boxplot([dec_scores, rec_scores], labels=['Deceased (n=56)', 'Recovered (n=155)'], patch_artist=True)
bp2['boxes'][0].set_facecolor('#d62728')
bp2['boxes'][1].set_facecolor('#2ca02c')
ax2.set_ylabel('Data Completeness Score')
ax2.set_title('Medical Record Data Completeness')

plt.tight_layout()
plt.savefig('/work/figure4_temperature_completeness.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 created.")

# Statistical tests
from scipy import stats
t_stat, p_val = stats.mannwhitneyu(deceased_temps, recovered_temps, alternative='two-sided')
print(f"Temperature Mann-Whitney U test: U={t_stat:.0f}, p={p_val:.4f}")
t_stat2, p_val2 = stats.mannwhitneyu(dec_scores, rec_scores, alternative='two-sided')
print(f"Completeness Mann-Whitney U test: U={t_stat2:.0f}, p={p_val2:.4f}")
print(f"Deceased temp median={np.median(deceased_temps):.2f}, mean={np.mean(deceased_temps):.2f}")
print(f"Recovered temp median={np.median(recovered_temps):.2f}, mean={np.mean(recovered_temps):.2f}")