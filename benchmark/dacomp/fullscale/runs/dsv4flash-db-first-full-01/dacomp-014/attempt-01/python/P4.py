import pandas as pd
import numpy as np

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Correlation matrix for engagement metrics
metrics = ['Views','Likes','Coins','Favorites','Shares','Comments','Danmaku Count','Overall Score','Creator Followers']
corr = df[metrics].corr(method='pearson')
print("Pearson correlations with Views:")
print(corr['Views'].sort_values(ascending=False).round(3))

print("\nFull correlation matrix (rounded):")
print(corr.round(3))

# Spearman rank correlation (more robust)
from scipy.stats import spearmanr
print("\nSpearman correlations with Views:")
for m in ['Likes','Coins','Favorites','Shares','Comments','Danmaku Count','Overall Score','Creator Followers']:
    rho, p = spearmanr(df['Views'], df[m])
    print(f"  {m}: {rho:.3f} (p={p:.2e})")