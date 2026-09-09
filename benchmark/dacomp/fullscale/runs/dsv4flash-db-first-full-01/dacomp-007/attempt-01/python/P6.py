import pandas as pd
import numpy as np

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)

# Overtime composition by department
print("=== OverTime composition by department ===")
print(pd.crosstab(df['Department'], df['OverTime'], normalize='index').round(3))

# Job role composition and attrition
print("\n=== Job role summary ===")
role_summary = df.groupby(['Department','JobRole']).agg(
    n=('is_attrition','size'),
    att=('is_attrition','sum'),
    att_rate=('is_attrition','mean'),
    avg_income=('MonthlyIncome','mean'),
    avg_level=('JobLevel','mean'),
    avg_age=('Age','mean'),
    avg_tenure=('YearsAtCompany','mean'),
    avg_twy=('TotalWorkingYears','mean'),
    pct_ot=('OverTime', lambda x: (x=='Yes').mean()),
    pct_single=('MaritalStatus', lambda x: (x=='Single').mean()),
    pct_stock0=('StockOptionLevel', lambda x: (x==0).mean()),
    pct_freq_travel=('BusinessTravel', lambda x: (x=='Travel_Frequently').mean())
).round(2)
print(role_summary.sort_values('att_rate'))

# Verify: check for any duplicate employee records / data quirks
print("\n=== Duplicate EmpID check ===")
print(f"Total rows: {len(df)}, unique EmpID: {df['EmpID'].nunique()}")
dup = df[df.duplicated('EmpID', keep=False)]
print(f"Duplicate EmpID rows: {len(dup)}")
print(dup.groupby('EmpID').size().sort_values(ascending=False).head(10))