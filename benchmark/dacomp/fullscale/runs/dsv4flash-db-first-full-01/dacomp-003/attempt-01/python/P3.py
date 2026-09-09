
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

china = db.frame(db.query("""
SELECT e."Year" AS year, e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China' ORDER BY e."Year"
"""))

prov = db.frame(db.query("""
SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"
"""))

# National: split phases
early = china[china['year'] <= 2007]
late = china[china['year'] >= 2008]
r_early, p_early = stats.pearsonr(early['pc_gdp'], early['ind_share'])
r_late, p_late = stats.pearsonr(late['pc_gdp'], late['ind_share'])
print(f"National 2000-2007 (rising phase): r = {r_early:.3f}, p = {p_early:.4f}")
print(f"National 2008-2018 (declining phase): r = {r_late:.3f}, p = {p_late:.4f}")
print(f"Peak share {china['ind_share'].max():.2f}% in {china.loc[china['ind_share'].idxmax(),'year']}")

# Province: correlation of initial share vs temporal slope
piv = prov.pivot_table(index='region', columns='year', values='ind_share')
initial = piv[2003]
delta = piv[2018] - piv[2003]
r_init_delta, p_init_delta = stats.pearsonr(initial, delta)
print(f"\nCorrelation between initial (2003) share and 2003-2018 change: r = {r_init_delta:.3f}, p = {p_init_delta:.4f}")
r_init_pearson, p_init_pearson = stats.pearsonr(initial, [stats.pearsonr(prov[prov['region']==r]['pc_gdp'], prov[prov['region']==r]['ind_share'])[0] for r in piv.index])
print(f"Correlation between initial share and province-level Pearson r: r = {r_init_pearson:.3f}, p = {p_init_pearson:.4f}")

# Within-province vs between-province decomposition of pooled correlation
prov_dm = prov.copy()
prov_dm['pc_dm'] = prov_dm['pc_gdp'] - prov_dm.groupby('region')['pc_gdp'].transform('mean')
prov_dm['sh_dm'] = prov_dm['ind_share'] - prov_dm.groupby('region')['ind_share'].transform('mean')
r_within, p_within = stats.pearsonr(prov_dm['pc_dm'], prov_dm['sh_dm'])
print(f"\nWithin-province (temporal, demeaned) Pearson r = {r_within:.3f}, p = {p_within:.5f}")

# Between-province: cross-sectional using means over time
means = prov.groupby('region')[['pc_gdp','ind_share']].mean()
r_between, p_between = stats.pearsonr(means['pc_gdp'], means['ind_share'])
print(f"Between-province (cross-sectional, time means) Pearson r = {r_between:.3f}, p = {p_between:.4f}")

# Rank correlation between region mean income and mean share
r_betw_s, p_betw_s = stats.spearmanr(means['pc_gdp'], means['ind_share'])
print(f"Between-province Spearman rho = {r_betw_s:.3f}, p = {p_betw_s:.4f}")

# Figure: initial share vs delta
fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(initial, delta, s=50, c=delta, cmap='coolwarm')
for i, r in enumerate(piv.index):
    ax.annotate(r.replace(' Province','').replace(' Municipality','').replace(' Zhuang Autonomous Region','').replace(' Uygur Autonomous Region','').replace(' Autonomous Region',''), (initial[i], delta[i]), fontsize=7, alpha=0.8)
coef = np.polyfit(initial, delta, 1)
xfit = np.linspace(initial.min(), initial.max(), 100)
ax.plot(xfit, np.polyval(coef, xfit), 'k--', alpha=0.6, label=f'OLS slope={coef[0]:.2f}')
ax.axhline(0, color='grey', lw=0.8)
ax.set_xlabel('Industrial water share in 2003 (%)')
ax.set_ylabel('Change in industrial water share 2003→2018 (pp)')
ax.set_title('Convergence: provinces with higher initial share decline more')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/fig_convergence.png', dpi=110)
plt.close()
print("\nSaved convergence figure.")
