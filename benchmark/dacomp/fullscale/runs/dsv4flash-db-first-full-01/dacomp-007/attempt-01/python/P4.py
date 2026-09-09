import pandas as pd
import numpy as np

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)

# Compare R&D vs Sales across key factors
print("=== MonthlyIncome by dept x job level ===")
print(df.groupby(['Department','JobLevel'])['MonthlyIncome'].agg(['count','mean','median']).round(0).unstack('Department'))

print("\n=== MonthlyIncome by dept x job level (R&D vs Sales) ===")
rd = df[df['Department']=='Research & Development']
sales = df[df['Department']=='Sales']
for lvl in [1,2,3,4,5]:
    rd_sub = rd[rd['JobLevel']==lvl]['MonthlyIncome']
    sa_sub = sales[sales['JobLevel']==lvl]['MonthlyIncome']
    print(f"Level {lvl}: R&D mean={rd_sub.mean():.0f} (n={len(rd_sub)}), Sales mean={sa_sub.mean():.0f} (n={len(sa_sub)})")

# Key factor comparison within job level 1 and 2
print("\n=== Job Level 1: factor comparison (R&D vs Sales) ===")
for factor in ['OverTime','MaritalStatus','BusinessTravel','StockOptionLevel','JobSatisfaction','EnvironmentSatisfaction']:
    tab = pd.crosstab([df.loc[df['JobLevel']==1,'Department'], df.loc[df['JobLevel']==1,factor]], df.loc[df['JobLevel']==1,'is_attrition'])
    # better: attrition rate by factor and dept
    sub = df[df['JobLevel']==1]
    rates = sub.groupby(['Department',factor])['is_attrition'].agg(['count','mean'])
    rates['rate'] = (rates['mean']*100).round(1)
    print(f"\n{factor} (JobLevel 1):")
    print(rates[['count','rate']].unstack('Department'))