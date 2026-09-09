import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/parsed_data.csv')

print("=== Average Showings by Decoration ===")
print(df.groupby('Decoration')['Showings'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Showings by Orientation ===")
print(df.groupby('Orientation')['Showings'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Showings by bedrooms ===")
print(df.groupby('bedrooms')['Showings'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Showings by floor category ===")
print(df.groupby('floor_category')['Showings'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Watch Count by Decoration ===")
print(df.groupby('Decoration')['Watch Count'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Watch Count by Orientation ===")
print(df.groupby('Orientation')['Watch Count'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Watch Count by bedrooms ===")
print(df.groupby('bedrooms')['Watch Count'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())
print("\n=== Average Watch Count by floor category ===")
print(df.groupby('floor_category')['Watch Count'].agg(['count','mean','median']).sort_values('mean', ascending=False).to_string())

# Correlation between Watch Count and Showings
corr, pval = stats.spearmanr(df['Watch Count'], df['Showings'])
print(f"\nSpearman corr(Watch Count, Showings) = {corr:.4f}, p={pval:.2e}")
pearson = np.corrcoef(df['Watch Count'], df['Showings'])[0,1]
print(f"Pearson corr = {pearson:.4f}")

# Watch count bins vs showings
df['watch_bin'] = pd.cut(df['Watch Count'], [-1,0,2,5,10,20,50,100,1000], labels=['0','1-2','3-5','6-10','11-20','21-50','51-100','100+'])
print("\n=== Avg Showings by Watch Count bin ===")
print(df.groupby('watch_bin')['Showings'].agg(['count','mean','median']).to_string())