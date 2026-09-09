
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

res = db.query("""
SELECT YearsAtCompany, Age, MonthlyIncome, PercentSalaryHike, JobSatisfaction,
       EnvironmentSatisfaction, WorkLifeBalance, JobInvolvement, RelationshipSatisfaction,
       PerformanceRating, StockOptionLevel, TrainingTimesLastYear, DistanceFromHome,
       NumCompaniesWorked, YearsSinceLastPromotion, YearsInCurrentRole, YearsWithCurrManager,
       JobLevel, TotalWorkingYears, DailyRate, HourlyRate, MonthlyRate
FROM sheet1
""")
df = db.frame(res)

corr = df.corr(numeric_only=True)['YearsAtCompany'].sort_values(ascending=False)
print("=== Correlations with YearsAtCompany ===")
print(corr.round(3).to_string())

# Save correlation table
corr.to_frame().round(3).to_csv('/work/corr_years.csv')

# Attrition comparison data for plots
res2 = db.query("""
SELECT YearsAtCompany, Attrition, MonthlyIncome, OverTime, StockOptionLevel,
       JobSatisfaction, YearsSinceLastPromotion, SalarySlab
FROM sheet1
""")
df2 = db.frame(res2)
df2['long_term'] = np.where(df2['YearsAtCompany'] >= 10, '10+ years', '<10 years')

print("\n=== Leaver vs Stayer stats overall ===")
print(df2.groupby('Attrition').agg(cnt=('YearsAtCompany','size'),
      avg_income=('MonthlyIncome','mean'),
      pct_overtime=('OverTime', lambda x: (x=='Yes').mean()*100),
      pct_no_stock=('StockOptionLevel', lambda x: (x==0).mean()*100)).round(2).to_string())

print("\n=== Long-term group: leaver vs stayer ===")
lt = df2[df2['long_term']=='10+ years']
print(lt.groupby('Attrition').agg(cnt=('YearsAtCompany','size'),
      avg_income=('MonthlyIncome','mean'),
      pct_overtime=('OverTime', lambda x: (x=='Yes').mean()*100),
      avg_years_since_promo=('YearsSinceLastPromotion','mean')).round(2).to_string())

# Save df2 for later figure building
df2.to_csv('/work/df_main.csv', index=False)
