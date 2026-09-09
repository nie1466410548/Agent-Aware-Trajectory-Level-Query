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

# Look at other factors: NumCompaniesWorked, DistanceFromHome, Training, YearsSinceLastPromotion
print("=== Attrition by NumCompaniesWorked buckets ===")
df['numcos_bucket'] = pd.cut(df['NumCompaniesWorked'], bins=[-1,0,1,2,4,9], labels=['0','1','2','3-4','5+'])
tab = df.groupby(['Department','numcos_bucket'])['is_attrition'].agg(['count','mean'])
tab['rate'] = (tab['mean']*100).round(1)
print(tab.reset_index().pivot(index='numcos_bucket', columns='Department', values='rate').round(1))
print("\nCounts:")
print(tab.reset_index().pivot(index='numcos_bucket', columns='Department', values='count'))

print("\n\n=== Attrition by DistanceFromHome buckets ===")
df['dist_bucket'] = pd.cut(df['DistanceFromHome'], bins=[-1,2,5,10,29], labels=['0-2','3-5','6-10','10+'])
tab2 = df.groupby(['Department','dist_bucket'])['is_attrition'].agg(['count','mean'])
tab2['rate'] = (tab2['mean']*100).round(1)
print(tab2.reset_index().pivot(index='dist_bucket', columns='Department', values='rate').round(1))

print("\n\n=== Attrition by YearsSinceLastPromotion ===")
df['promo_bucket'] = pd.cut(df['YearsSinceLastPromotion'], bins=[-1,0,1,3,9], labels=['0','1','2-3','4+'])
tab3 = df.groupby(['Department','promo_bucket'])['is_attrition'].agg(['count','mean'])
tab3['rate'] = (tab3['mean']*100).round(1)
print(tab3.reset_index().pivot(index='promo_bucket', columns='Department', values='rate').round(1))
print("\nCounts:")
print(tab3.reset_index().pivot(index='promo_bucket', columns='Department', values='count'))

print("\n\n=== Attrition by TrainingTimesLastYear ===")
tab4 = df.groupby(['Department','TrainingTimesLastYear'])['is_attrition'].agg(['count','mean'])
tab4['rate'] = (tab4['mean']*100).round(1)
print(tab4.reset_index().pivot(index='TrainingTimesLastYear', columns='Department', values='rate').round(1))