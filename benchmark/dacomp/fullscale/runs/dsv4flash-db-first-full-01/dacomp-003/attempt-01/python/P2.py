
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
os.makedirs('work', exist_ok=True)

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

# ---- National figures ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.plot(china['year'], china['pc_gdp'], 'o-', color='tab:blue', label='Per capita GDP (yuan)')
ax.set_ylabel('Per capita GDP (yuan/person)', color='tab:blue')
ax.set_xlabel('Year')
ax2 = ax.twinx()
ax2.plot(china['year'], china['ind_share'], 's--', color='tab:red', label='Industrial water share (%)')
ax2.set_ylabel('Industrial water share (%)', color='tab:red')
ax.set_title('China: GDP per capita vs industrial water share, 2000-2018')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1+lines2, labels1+labels2, loc='center left')
ax.grid(alpha=0.3)

ax = axes[1]
ax.scatter(china['pc_gdp'], china['ind_share'], c=china['year'], cmap='viridis', s=60)
# quadratic fit
coef = np.polyfit(china['pc_gdp'], china['ind_share'], 2)
xfit = np.linspace(china['pc_gdp'].min(), china['pc_gdp'].max(), 200)
ax.plot(xfit, np.polyval(coef, xfit), 'k--', alpha=0.7, label='Quadratic fit')
r2 = 1 - np.sum((china['ind_share']-np.polyval(coef, china['pc_gdp']))**2)/np.sum((china['ind_share']-china['ind_share'].mean())**2)
ax.set_xlabel('Per capita GDP (yuan/person)')
ax.set_ylabel('Industrial water share (%)')
ax.set_title(f'National scatter (R² quadratic = {r2:.3f})')
cb = plt.colorbar(ax.collections[0], ax=ax)
cb.set_label('Year')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/fig_national.png', dpi=110)
plt.close()

# ---- Province figures: scatter of pooled data colored by region, plus temporal slope ----
# Temporal change: share in 2018 vs 2003
piv = prov.pivot_table(index='region', columns='year', values='ind_share')
change = piv[2018] - piv[2003]
pcgdp_2018 = prov[prov['year']==2018].set_index('region')['pc_gdp']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
ax.scatter(prov['pc_gdp'], prov['ind_share'], s=12, alpha=0.45)
ax.set_xlabel('Per capita GDP (yuan/person)')
ax.set_ylabel('Industrial water share (%)')
ax.set_title('All province-year observations (n=496)')
ax.grid(alpha=0.3)

ax = axes[1]
sc = ax.scatter(pcgdp_2018, change, c=change, cmap='coolwarm', s=60)
ax.axhline(0, color='k', lw=0.8)
ax.set_xlabel('Per capita GDP 2018 (yuan/person)')
ax.set_ylabel('Change in industrial water share 2003→2018 (pp)')
ax.set_title('Temporal change in industrial water share vs 2018 income level')
plt.colorbar(sc, ax=ax, label='Δ share (pp)')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/fig_province_changes.png', dpi=110)
plt.close()

# save intermediate summaries
change_df = pd.DataFrame({'region': change.index, 'delta_share_pp': change.values})
change_df = change_df.merge(pcgdp_2018.rename('pc_gdp_2018'), on='region')
change_df.to_csv('work/province_change_summary.csv', index=False)
print(change_df.sort_values('delta_share_pp').to_string())
