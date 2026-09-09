import pandas as pd
import numpy as np
from scipy.stats import spearmanr

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Overall Score correlation with metrics
print("=== Correlations with Overall Score ===")
for m in ['Views','Likes','Coins','Favorites','Shares','Comments','Danmaku Count','Creator Followers']:
    rho, p = spearmanr(df['Overall Score'], df[m])
    print(f"  {m}: rho={rho:.3f}")

# What does Overall Score correlate most with? Check ratio metrics
print("\n=== Multiple regression-ish: which metrics best predict Overall Score ===")
import statsmodels.api as sm
# Check if statsmodels available
try:
    X = df[['Likes','Coins','Favorites','Shares','Comments','Danmaku Count','Views']].copy()
    X = sm.add_constant(X)
    y = df['Overall Score']
    model = sm.OLS(y, X).fit()
    print(model.params.round(4))
    print("R-squared:", round(model.rsquared, 4))
except Exception as e:
    print("statsmodels not available:", e)

# Top 20 videos by Overall Score
print("\n=== Top 20 Videos by Overall Score ===")
cols = ['Title','Creator','Overall Score','Views','Likes','Coins','Favorites','Shares','Video Category','Creator Followers']
for _, row in df.sort_values('Overall Score', ascending=False).head(20).iterrows():
    print(f"  Score: {row['Overall Score']:>8}, Views: {row['Views']:>8}, Category: {str(row['Video Category']):>20}, Creator: {row['Creator'][:22]}")