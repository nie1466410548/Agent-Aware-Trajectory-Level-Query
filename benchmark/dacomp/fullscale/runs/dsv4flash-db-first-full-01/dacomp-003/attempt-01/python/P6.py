
import numpy as np
import pandas as pd
from scipy import stats

prov = db.frame(db.query("""
SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"
"""))

piv = prov.pivot_table(index='region', columns='year', values='ind_share')
gdp_piv = prov.pivot_table(index='region', columns='year', values='pc_gdp')
initial_share = piv[2003]
initial_gdp = gdp_piv[2003]
delta = piv[2018] - piv[2003]

r1, p1 = stats.pearsonr(initial_gdp, delta)
r2, p2 = stats.spearmanr(initial_gdp, delta)
print(f"2003 GDP vs 2003-2018 change in share: Pearson r = {r1:.3f}, p = {p1:.4f}; Spearman = {r2:.3f}, p = {p2:.4f}")

r3, p3 = stats.pearsonr(initial_gdp, initial_share)
print(f"2003 GDP vs 2003 share: r = {r3:.3f}, p = {p3:.4f}")

# Show delta vs initial gdp sorted
out = pd.DataFrame({'region': piv.index, 'pc_gdp_2003': initial_gdp.values, 'initial_share_2003': initial_share.values, 'delta_share_pp': delta.values})
print(out.sort_values('delta_share_pp').to_string())
