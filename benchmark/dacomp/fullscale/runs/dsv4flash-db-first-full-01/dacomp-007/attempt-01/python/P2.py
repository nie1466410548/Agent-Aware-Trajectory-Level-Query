import pandas as pd
import numpy as np

result = db.query("SELECT Department, JobLevel, Attrition FROM sheet1")
df = db.frame(result)

# Attrition rate by dept and job level
pivot = df.groupby(['Department','JobLevel'])['Attrition'].apply(lambda x: (x=='Yes').mean()*100).unstack()
print("Attrition rate (%) by dept x job level:")
print(pivot.round(2))

# Composition (% employees by level) per dept
comp = df.groupby(['Department','JobLevel']).size().unstack(fill_value=0)
comp_pct = comp.div(comp.sum(axis=1), axis=0)*100
print("\nComposition (% of dept) by job level:")
print(comp_pct.round(1))

# Standardization: apply R&D's job-level attrition rates to Sales' composition
# Counterfactual: what would R&D attrition be if it had Sales composition?
levels = sorted(set(df['JobLevel']))
# Use pooled per-level rates as reference? Instead do direct standardization.

# Direct standardization using each dept's own rates applied to overall (company) composition
overall_comp = df.groupby('JobLevel').size()
overall_comp_pct = overall_comp/overall_comp.sum()

std_rates = {}
for dept in ['Sales','Research & Development','Human Resources']:
    rates = pivot.loc[dept]
    std_rates[dept] = (rates * overall_comp_pct).sum()
print("\nCompany-standardized attrition rate (%):")
for k,v in std_rates.items():
    print(f"  {k}: {v:.2f}")

# Counterfactual: Sales attrition rate if it had R&D composition (use Sales' level-specific rates)
rates_sales = pivot.loc['Sales']
cf_sales_composition_RD = (rates_sales * comp_pct.loc['Research & Development']/100).sum()
print(f"\nSales attrition if it had R&D's job-level composition: {cf_sales_composition_RD:.2f}%")

# Counterfactual: R&D attrition rate if it had Sales composition
rates_rd = pivot.loc['Research & Development']
cf_rd_composition_Sales = (rates_rd * comp_pct.loc['Sales']/100).sum()
print(f"R&D attrition if it had Sales' job-level composition: {cf_rd_composition_Sales:.2f}%")

# Counterfactual: apply Sales level rates to R&D composition => expected Sales-like rate given R&D comp
# and apply R&D rates to Sales comp
actual_sales = 20.67
actual_rd = 13.75
print(f"\nActual: Sales={actual_sales}%, R&D={actual_rd}%, diff={actual_sales-actual_rd:.2f}pp")
print(f"Composition effect (if only composition differed): {actual_sales - cf_rd_composition_Sales:.2f}pp")
print(f"Rate effect (if only level-specific rates differed): {cf_rd_composition_Sales - actual_rd:.2f}pp")