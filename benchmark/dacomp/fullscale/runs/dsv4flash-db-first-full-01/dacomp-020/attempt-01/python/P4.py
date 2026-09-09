
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')
mh = df['Mental health score'].values.astype(float)
exam = df['Exam score'].values

# --- Q1: Bivariate relationship ---
r_pearson, p_pearson = stats.pearsonr(mh, exam)
r_spearman, p_spearman = stats.spearmanr(mh, exam)
r_kendall, p_kendall = stats.kendalltau(mh, exam)
print(f"Pearson r={r_pearson:.4f}, p={p_pearson:.3e}")
print(f"Spearman rho={r_spearman:.4f}, p={p_spearman:.3e}")
print(f"Kendall tau={r_kendall:.4f}, p={p_kendall:.3e}")

# Linear regression
slope, intercept, r_lin, p_lin, se_slope = stats.linregress(mh, exam)
print(f"OLS: exam = {intercept:.3f} + {slope:.3f}*MH, R^2={r_lin**2:.4f}, p={p_lin:.3e}, se(slope)={se_slope:.4f}")

# Effect size: per 1-unit MH increase
print(f"Effect per 1 MH point: {slope:.3f} exam points; per 5-point span (1->6): {5*slope:.3f}")

# Polynomial fits: 1,2,3,4 degree
X = mh
y = exam
n = len(y)
def polyfit(deg):
    coef = np.polyfit(X, y, deg)
    yhat = np.polyval(coef, X)
    rss = np.sum((y-yhat)**2)
    k = deg + 1
    r2 = 1 - rss/np.sum((y-y.mean())**2)
    aic = n*np.log(rss/n) + 2*k
    bic = n*np.log(rss/n) + k*np.log(n)
    return coef, r2, rss, aic, bic, yhat

for deg in [1,2,3,4]:
    coef, r2, rss, aic, bic, yhat = polyfit(deg)
    print(f"deg{deg}: R2={r2:.5f}, RSS={rss:.1f}, AIC={aic:.1f}, BIC={bic:.1f}, coefs={np.round(coef,4)}")

# F-test for adding quadratic term (linear vs quadratic)
coef1, r2_1, rss1, aic1, bic1, _ = polyfit(1)
coef2, r2_2, rss2, aic2, bic2, _ = polyfit(2)
coef3, r2_3, rss3, aic3, bic3, _ = polyfit(3)

def ftest(rss_r, rss_f, df_extra, df_resid_f):
    f = ((rss_r - rss_f)/df_extra) / (rss_f/df_resid_f)
    p = 1 - stats.f.cdf(f, df_extra, df_resid_f)
    return f, p

f, p = ftest(rss1, rss2, 1, n-3)
print(f"F-test linear vs quadratic: F={f:.3f}, p={p:.4f}")
f2, p2 = ftest(rss2, rss3, 1, n-4)
print(f"F-test quadratic vs cubic: F={f2:.3f}, p={p2:.4f}")

# Group means with confidence intervals (for inflection detection)
g = df.groupby('Mental health score')['Exam score']
gm = g.mean()
gn = g.count()
gs = g.std(ddof=0)
se = gs/np.sqrt(gn)
print("\nMH  n  mean  se  CI_low  CI_high")
for v in gm.index:
    ci = stats.t.ppf(0.975, gn[v]-1)*se[v]
    print(f"{v:3d} {gn[v]:4d} {gm[v]:6.2f} {se[v]:5.2f} {gm[v]-ci:6.2f} {gm[v]+ci:6.2f}")

# consecutive differences
diffs = gm.diff()
print("\nConsecutive group-mean differences:")
print(np.round(diffs,2))
