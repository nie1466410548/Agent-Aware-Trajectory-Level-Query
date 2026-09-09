import pandas as pd
import numpy as np

df = pd.read_csv('/work/final_classification.csv')
print("Excellent HP stats:")
ex = df[df['classification']=='Excellent']
print(f" HP total sum: {ex['hp_total'].sum()}, HP completed sum: {ex['hp_completed'].sum()}")
print(f" Owners with hp_total>0: {(ex['hp_total']>0).sum()}/{len(ex)}")
print(f" HP completion rate: {ex['hp_completed'].sum()/ex['hp_total'].sum():.3f}")

print("\nGood HP stats:")
gd = df[df['classification']=='Good']
print(f" HP total sum: {gd['hp_total'].sum()}, HP completed sum: {gd['hp_completed'].sum()}")
print(f" Owners with hp_total>0: {(gd['hp_total']>0).sum()}/{len(gd)}")

print("\nNeeds HP stats:")
ni = df[df['classification']=='Needs Improvement']
print(f" HP total sum: {ni['hp_total'].sum()}, HP completed sum: {ni['hp_completed'].sum()}")
print(f" Owners with hp_total>0: {(ni['hp_total']>0).sum()}/{len(ni)}")