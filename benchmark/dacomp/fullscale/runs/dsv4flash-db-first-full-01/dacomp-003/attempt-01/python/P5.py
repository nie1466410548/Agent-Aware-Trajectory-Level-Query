
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

# Pooled quadratic fit (gives inverted-U if coef negative)
x = prov['pc_gdp'].values; y = prov['ind_share'].values
coef = np.polyfit(x, y, 2)
pred = np.polyval(coef, x)
r2 = 1 - np.sum((y-pred)**2)/np.sum((y-y.mean())**2)
vertex = -coef[1]/(2*coef[0])
print(f"Pooled quadratic: y = {coef[0]:.3e} x² + {coef[1]:.4f} x + {coef[2]:.2f}, R²={r2:.3f}, vertex x={vertex:,.0f} yuan")
print(f"Interpretation: quadratic coefficient sign = {'positive (U-shape)' if coef[0]>0 else 'negative (inverted-U)'}")

# Province level trend slopes (linear fit of share vs year) - which provinces rise/fall
slopes = {}
for reg, g in prov.groupby('region'):
    slopes[reg] = np.polyfit(g['year'], g['ind_share'], 1)[0]
sdf = pd.DataFrame({'region': list(slopes.keys()), 'annual_pp_change': list(slopes.values())}).sort_values('annual_pp_change')
print("\nTop 5 declining provinces (annual pp/yr):")
print(sdf.head().to_string())
print("Top 5 rising provinces:")
print(sdf.tail().to_string())

# Representative series
rep = ['Shanghai Municipality','Heilongjiang Province','Jiangsu Province','Xinjiang Uygur Autonomous Region','China']
fig, ax = plt.subplots(figsize=(9,6))
for r in rep:
    g = prov[prov['region']==r]
    lbl = r.replace(' Municipality','').replace(' Province','').replace(' Uygur Autonomous Region','')
    ax.plot(g['year'], g['ind_share'], 'o-', label=lbl)
ax.set_xlabel('Year'); ax.set_ylabel('Industrial water share (%)')
ax.set_title('Divergent trajectories across provinces')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('work/fig_trajectories.png', dpi=110); plt.close()
print("\nSaved trajectories figure.")

# Also examine whether more developed provinces systematically at higher share (2018 snapshot)
g18 = prov[prov['year']==2018]
r18, p18 = stats.pearsonr(g18['pc_gdp'], g18['ind_share'])
print(f"\n2018 cross-section: r = {r18:.3f}, p = {p18:.4f}")
g03 = prov[prov['year']==2003]
r03, p03 = stats.pearsonr(g03['pc_gdp'], g03['ind_share'])
print(f"2003 cross-section: r = {r03:.3f}, p = {p03:.4f}")
