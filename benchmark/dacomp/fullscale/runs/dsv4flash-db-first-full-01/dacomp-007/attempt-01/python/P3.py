import pandas as pd
import numpy as np

result = db.query("SELECT Department, JobLevel, Attrition FROM sheet1")
df = db.frame(result)

# Attrition rates by dept and job level
pivot = df.groupby(['Department','JobLevel'])['Attrition'].apply(lambda x: (x=='Yes').mean()*100).unstack()
print("Attrition rates by dept x job level:")
print(pivot.round(2))

# Composition by dept
comp = df.groupby(['Department','JobLevel']).size().unstack(fill_value=0)
comp_pct = comp.div(comp.sum(axis=1), axis=0)*100
print("\nComposition by dept:")
print(comp_pct.round(1))

# Overall composition (company-wide)
overall = df.groupby('JobLevel').size()
overall_pct = overall/overall.sum()*100
print("\nOverall company composition:")
print(overall_pct.round(1))

# Decomposition: Oaxaca-like
# Reference = overall company composition
# What would Sales' attrition be if it had overall composition?
sales_rates = pivot.loc['Sales']
rd_rates = pivot.loc['Research & Development']

# Standardized rate effect (using overall composition as reference)
sales_std = (sales_rates * overall_pct/100).sum()
rd_std = (rd_rates * overall_pct/100).sum()
print(f"\n--- Standardized rates (company composition) ---")
print(f"Sales: {sales_std:.2f}%")
print(f"R&D: {rd_std:.2f}%")
print(f"Rate effect (difference in standardized rates): {sales_std - rd_std:.2f}pp")

# Composition effect
actual_sales = 20.67
actual_rd = 13.75
print(f"\nActual sales: {actual_sales}%")
print(f"Actual R&D: {actual_rd}%")
print(f"Actual difference: {actual_sales - actual_rd:.2f}pp")
print(f"Composition effect (actual diff - rate effect): {(actual_sales-actual_rd) - (sales_std-rd_std):.2f}pp")

# Alternative: Pure decomposition
# If we use R&D composition as reference:
# Rate effect = apply Sales rates to R&D comp - apply R&D rates to R&D comp
rate_eff_rdref = (sales_rates * comp_pct.loc['Research & Development']/100).sum() - actual_rd
print(f"\n--- Decomposition with R&D composition as reference ---")
print(f"Rate effect (Sales rates - R&D rates, with R&D comp): {rate_eff_rdref:.2f}pp")
# Composition effect = apply Sales rates to Sales comp - apply Sales rates to R&D comp
comp_eff_salesref = actual_sales - (sales_rates * comp_pct.loc['Research & Development']/100).sum()
print(f"Composition effect (Sales comp - R&D comp, with Sales rates): {comp_eff_salesref:.2f}pp")
print(f"Total: {rate_eff_rdref + comp_eff_salesref:.2f}pp")

# Using Sales composition as reference
rate_eff_salesref = actual_sales - (rd_rates * comp_pct.loc['Sales']/100).sum()
print(f"\n--- Decomposition with Sales composition as reference ---")
print(f"Rate effect (Sales rates - R&D rates, with Sales comp): {rate_eff_salesref:.2f}pp")
comp_eff_rdref = (rd_rates * comp_pct.loc['Sales']/100).sum() - actual_rd
print(f"Composition effect (Sales comp - R&D comp, with R&D rates): {comp_eff_rdref:.2f}pp")
print(f"Total: {rate_eff_salesref + comp_eff_rdref:.2f}pp")