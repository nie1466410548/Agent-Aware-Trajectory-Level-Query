import pandas as pd
import numpy as np

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Standardize and do multiple linear regression with numpy
metrics = ['Views','Likes','Coins','Favorites','Shares','Comments','Danmaku Count']
X = df[metrics].values.astype(float)
y = df['Overall Score'].values.astype(float)

# Add constant
Xc = np.column_stack([np.ones(len(X)), X])
beta, res, rank, sv = np.linalg.lstsq(Xc, y, rcond=None)
pred = Xc @ beta
ss_res = np.sum((y - pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
print("Regression coefficients (standardized data):")
# Standardized coefficients
Xz = (X - X.mean(axis=0)) / X.std(axis=0)
Xzc = np.column_stack([np.ones(len(Xz)), Xz])
beta_z, _, _, _ = np.linalg.lstsq(Xzc, y, rcond=None)
for m, b in zip(metrics, beta_z[1:]):
    print(f"  {m}: {b:.3f}")
print(f"R-squared (raw): {r2:.4f}")

# Top 20 videos by Overall Score
print("\n=== Top 20 Videos by Overall Score ===")
cols = ['Title','Creator','Overall Score','Views','Likes','Coins','Favorites','Shares','Video Category','Creator Followers']
top = df.sort_values('Overall Score', ascending=False).head(20)
for _, row in top.iterrows():
    print(f"  Score: {row['Overall Score']:>8}, Views: {row['Views']:>8}, Category: {str(row['Video Category']):>20}, Creator: {row['Creator'][:22]}")