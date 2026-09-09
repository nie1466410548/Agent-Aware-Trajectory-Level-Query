import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)
df = df.drop_duplicates(subset='EmpID', keep='first')

# Manager comparison across departments
print("=== Manager Role Across Departments ===")
mgr = df[df['JobRole']=='Manager']
print(mgr.groupby('Department').agg(
    n=('EmpID','count'),
    att_rate=('is_attrition','mean'),
    avg_income=('MonthlyIncome','mean'),
    avg_level=('JobLevel','mean'),
    avg_tenure=('YearsAtCompany','mean'),
    avg_age=('Age','mean'),
    pct_ot=('OverTime', lambda x: (x=='Yes').mean())
).round(2))

print("\n\n=== Key R&D Sales Representative role comparison ===")
# Compare Sales Reps with R&D roles that have similar characteristics
sd = df[df['Department']=='Sales']
rd = df[df['Department']=='Research & Development']
print(f"Sales Reps: n={len(sd[sd['JobRole']=='Sales Representative'])}, att={sd[sd['JobRole']=='Sales Representative']['is_attrition'].mean()*100:.1f}%")
print(f"Sales Execs: n={len(sd[sd['JobRole']=='Sales Executive'])}, att={sd[sd['JobRole']=='Sales Executive']['is_attrition'].mean()*100:.1f}%")

# What if Sales Reps had the same attrition rate as the next lowest role?
print("\n\n=== Counterfactual: What if Sales Reps had attrition like Lab Techs? ===")
sales_reps = df[df['JobRole']=='Sales Representative']
actual_sales_att = df[df['Department']=='Sales']['is_attrition'].sum()
actual_sales_n = len(df[df['Department']=='Sales'])
actual_sales_rate = actual_sales_att/actual_sales_n*100
print(f"Actual Sales attrition: {actual_sales_att}/{actual_sales_n} = {actual_sales_rate:.1f}%")

# If Sales Reps had same rate as Lab Techs (23.75%)
lab_tech_rate = df[df['JobRole']=='Laboratory Technician']['is_attrition'].mean()
new_sales_rep_att = lab_tech_rate * len(sales_reps)
new_sales_att = actual_sales_att - sales_reps['is_attrition'].sum() + new_sales_rep_att
new_sales_rate = new_sales_att/actual_sales_n*100
print(f"If Sales Reps had Lab Tech rate ({lab_tech_rate*100:.1f}%): {new_sales_att:.0f}/{actual_sales_n} = {new_sales_rate:.1f}%")

# If Sales Reps had same rate as R&D level 1 avg
rd_l1_rate = df[(df['Department']=='Research & Development') & (df['JobLevel']==1)]['is_attrition'].mean()
new_sales_rep_att2 = rd_l1_rate * len(sales_reps)
new_sales_att2 = actual_sales_att - sales_reps['is_attrition'].sum() + new_sales_rep_att2
new_sales_rate2 = new_sales_att2/actual_sales_n*100
print(f"If Sales Reps had R&D L1 rate ({rd_l1_rate*100:.1f}%): {new_sales_att2:.0f}/{actual_sales_n} = {new_sales_rate2:.1f}%")

# Detailed breakdown of what contributes to the gap
print("\n\n=== Decomposition of the R&D-Sales attrition gap ===")
# The gap is 20.67 - 13.75 = 6.92pp
# Let's see how much of this gap is explained by different factors

# Let's compute the percentage of Sales attrition that comes from Sales Reps
sales_rep_att = sales_reps['is_attrition'].sum()
print(f"Sales Reps contribute {sales_rep_att}/{actual_sales_att} = {sales_rep_att/actual_sales_att*100:.1f}% of Sales attrition")
print(f"Sales Reps are {len(sales_reps)}/{actual_sales_n} = {len(sales_reps)/actual_sales_n*100:.1f}% of Sales employees")

# Similarly, the Lab Techs in R&D
lab_techs = df[df['JobRole']=='Laboratory Technician']
rd_att = df[df['Department']=='Research & Development']['is_attrition'].sum()
rd_n = len(df[df['Department']=='Research & Development'])
print(f"\nLab Techs contribute {lab_techs['is_attrition'].sum()}/{rd_att} = {lab_techs['is_attrition'].sum()/rd_att*100:.1f}% of R&D attrition")
print(f"Lab Techs are {len(lab_techs)}/{rd_n} = {len(lab_techs)/rd_n*100:.1f}% of R&D employees")