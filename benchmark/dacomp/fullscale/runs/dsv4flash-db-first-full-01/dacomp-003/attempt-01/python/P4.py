import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

prov = db.frame(db.query("""
SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"
"""))

piv = prov.pivot_table(index='region', columns='year', values='ind_share')
initial = piv[2003].values
delta = (piv[2018] - piv[2003]).values
regions = piv.index.tolist()

# Shorten region names
short = [r.replace(' Province','').replace(' Municipality','').replace(' Zhuang Autonomous Region','').replace(' Uygur Autonomous Region','').replace(' Autonomous Region','') for r in regions]

# Convergence figure
fig, ax = plt.subplots(figsize=(10, 7))
sc = ax.scatter(initial, delta, s=60, c=delta, cmap='coolwarm', edgecolors='k', linewidth=0.5)
for i, r in enumerate(short):
    ax.annotate(r, (initial[i], delta[i]), fontsize=7, alpha=0.8)
coef = np.polyfit(initial, delta, 1)
xfit = np.linspace(initial.min(), initial.max(), 100)
ax.plot(xfit, np.polyval(coef, xfit), 'k--', alpha=0.6, label=f'OLS slope = {coef[0]:.2f}')
ax.axhline(0, color='grey', lw=0.8)
ax.set_xlabel('Industrial water share in 2003 (%)')
ax.set_ylabel('Change in industrial water share 2003→2018 (pp)')
ax.set_title('Convergence pattern: provinces with higher initial share tend to decline more')
ax.legend()
ax.grid(alpha=0.3)
plt.colorbar(sc, ax=ax, label='Δ share (pp)')
plt.tight_layout()
plt.savefig('work/fig_convergence.png', dpi=110)
plt.close()
print("Saved convergence figure.")

# Between-province cross-sectional: means over time
means = prov.groupby('region')[['pc_gdp','ind_share']].mean().values
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(means[:,0], means[:,1], s=60, c='steelblue', edgecolors='k')
for i, r in enumerate(short):
    ax.annotate(r, (means[i,0], means[i,1]), fontsize=7, alpha=0.8)
ax.set_xlabel('Mean per capita GDP (yuan/person)')
ax.set_ylabel('Mean industrial water share (%)')
ax.set_title('Cross-sectional (between-province): richer provinces use more industrial water')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/fig_between_province.png', dpi=110)
plt.close()
print("Saved between-province figure.")

# Within-province: demeaned scatter
prov_dm = prov.copy()
prov_dm['pc_dm'] = prov_dm['pc_gdp'] - prov_dm.groupby('region')['pc_gdp'].transform('mean')
prov_dm['sh_dm'] = prov_dm['ind_share'] - prov_dm.groupby('region')['ind_share'].transform('mean')
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(prov_dm['pc_dm'], prov_dm['sh_dm'], s=10, alpha=0.4, c='forestgreen')
ax.axhline(0, color='grey', lw=0.5)
ax.axvline(0, color='grey', lw=0.5)
ax.set_xlabel('Within-province deviation of per capita GDP (yuan/person)')
ax.set_ylabel('Within-province deviation of industrial water share (pp)')
ax.set_title('Within-province (temporal): as a province develops, its industrial water share falls')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/fig_within_province.png', dpi=110)
plt.close()
print("Saved within-province figure.")