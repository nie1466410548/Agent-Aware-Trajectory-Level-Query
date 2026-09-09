
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('work', exist_ok=True)

# Load national-level data (already computed in SQL S16)
china = db.frame(db.query("""
SELECT e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" AS ind_w,
       s."Total Water Consumption (100 million m³) " AS tot_w,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China'
ORDER BY e."Year"
"""))
print(china.to_string())

# National-level correlation
r_p, p_p = stats.pearsonr(china['pc_gdp'], china['ind_share'])
r_s, p_s = stats.spearmanr(china['pc_gdp'], china['ind_share'])
print(f"\nNational Pearson r = {r_p:.4f}, p = {p_p:.4f}")
print(f"National Spearman rho = {r_s:.4f}, p = {p_s:.4f}")

# Load province data (from S17)
prov = db.frame(db.query("""
SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China'
ORDER BY e."Region Name", e."Year"
"""))
print("\nProvince rows:", len(prov), "regions:", prov['region'].nunique())

# Province-level correlations
prov_corr = []
for reg, g in prov.groupby('region'):
    if g['ind_share'].nunique() < 3:
        continue
    r_p, p_p = stats.pearsonr(g['pc_gdp'], g['ind_share'])
    r_s, p_s = stats.spearmanr(g['pc_gdp'], g['ind_share'])
    prov_corr.append({'region': reg, 'pearson_r': r_p, 'pearson_p': p_p,
                      'spearman_rho': r_s, 'spearman_p': p_s,
                      'start_pc': g['pc_gdp'].min(), 'end_pc': g['pc_gdp'].max(),
                      'start_share': g['ind_share'].min(), 'end_share': g['ind_share'].max(),
                      'mean_share': g['ind_share'].mean()})
pc = pd.DataFrame(prov_corr)
print("\nProvince-level Pearson correlations (summary):")
print(pc[['region','pearson_r','pearson_p','mean_share']].sort_values('pearson_r').to_string())

# Overall pooled correlation across all province-year observations
r_pool, p_pool = stats.pearsonr(prov['pc_gdp'], prov['ind_share'])
r_pool_s, p_pool_s = stats.spearmanr(prov['pc_gdp'], prov['ind_share'])
print(f"\nPooled province-year Pearson r = {r_pool:.4f}, p = {p_pool:.4f}")
print(f"Pooled province-year Spearman rho = {r_pool_s:.4f}, p = {p_pool_s:.4f}")
