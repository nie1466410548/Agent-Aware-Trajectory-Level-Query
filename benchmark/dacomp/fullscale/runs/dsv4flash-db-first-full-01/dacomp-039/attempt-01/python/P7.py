import pandas as pd
import numpy as np
from scipy import stats

rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)

def onehot(df, cols):
    X = np.ones((len(df), 1))
    for c in cols:
        dummies = pd.get_dummies(df[c], prefix=c, drop_first=True)
        X = np.hstack([X, dummies.values])
    return X

def r2(X, y):
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = ((y - pred)**2).sum()
    ss_tot = ((y - y.mean())**2).sum()
    return 1 - ss_res/ss_tot

y = df['Churn Rate'].values
yr = df['Level Rating'].values

X_diff = onehot(df, ['Difficulty Level'])
X_type = onehot(df, ['Level Type'])

# Interaction model: difficulty*type onehot
df['comb'] = df['Difficulty Level'] + '|' + df['Level Type']
X_comb = onehot(df, ['comb'])

print("=== R2 for Churn Rate ===")
print(f"Difficulty only:    {r2(X_diff, y):.4f}")
print(f"Type only:          {r2(X_type, y):.4f}")
print(f"Difficulty + Type:  {r2(np.hstack([X_diff, X_type[:,1:]]), y):.4f}")
print(f"Full interaction:   {r2(X_comb, y):.4f}")

print("\n=== R2 for Level Rating ===")
print(f"Difficulty only:    {r2(X_diff, yr):.4f}")
print(f"Type only:          {r2(X_type, yr):.4f}")
print(f"Difficulty + Type:  {r2(np.hstack([X_diff, X_type[:,1:]]), yr):.4f}")
print(f"Full interaction:   {r2(X_comb, yr):.4f}")

# Cohen's d / effect size: compare difficulty levels pairwise (Hell vs Hard etc.)
print("\n=== Pairwise t-tests for Churn Rate across difficulty ===")
for a, b in [('Easy','Normal'), ('Normal','Hard'), ('Hard','Hell (Difficulty Level)')]:
    x = df[df['Difficulty Level']==a]['Churn Rate']
    z = df[df['Difficulty Level']==b]['Churn Rate']
    t, p = stats.ttest_ind(x, z, equal_var=False)
    # Cohen's d
    sp = np.sqrt(( (len(x)-1)*x.var() + (len(z)-1)*z.var() ) / (len(x)+len(z)-2))
    d = (z.mean()-x.mean())/sp
    print(f"{a} vs {b}: mean diff={z.mean()-x.mean():.4f}, t={t:.1f}, p={p:.2e}, Cohen's d={d:.2f}")

print("\n=== Pairwise t-tests for Churn Rate across Type (within Hard, largest group) ===")
hd = df[df['Difficulty Level']=='Hard']
for a, b in [('Parkour','Puzzle'), ('Puzzle','Battle'), ('Battle','BOSS')]:
    x = hd[hd['Level Type']==a]['Churn Rate']
    z = hd[hd['Level Type']==b]['Churn Rate']
    t, p = stats.ttest_ind(x, z, equal_var=False)
    sp = np.sqrt(( (len(x)-1)*x.var() + (len(z)-1)*z.var() ) / (len(x)+len(z)-2))
    d = (z.mean()-x.mean())/sp
    print(f"{a} vs {b}: mean diff={z.mean()-x.mean():.4f}, t={t:.1f}, p={p:.2e}, Cohen's d={d:.2f}")