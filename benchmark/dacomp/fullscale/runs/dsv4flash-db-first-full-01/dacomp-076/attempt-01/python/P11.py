import pandas as pd, numpy as np
from scipy import stats

df = pd.read_pickle('/work/df_final.pkl')

# ---- Correlation of retention_probability with candidate dimensions ----
feat_corr = ['comprehensive_customer_score','total_revenue','transaction_count',
             'avg_transactions_per_month','transaction_value_volatility','tx_ratio',
             'seasonal_std','seasonal_max_share','seasonal_entropy','seasonal_cv',
             'score_rev_resid','rev_per_tx','customer_age_days']

print("=== CORRELATION WITH retention_probability (full dataset) ===")
for f in feat_corr:
    r, p = stats.pearsonr(df[f].dropna(), df['retention_probability'][df[f].notna()])
    rho, p_s = stats.spearmanr(df[f].dropna(), df['retention_probability'][df[f].notna()])
    print(f"  {f:35s} Pearson r={r:+.3f} (p={p:.4f})   Spearman rho={rho:+.3f} (p={p_s:.4f})")

# ---- Within anomaly-prone segments ----
print("\n=== CORRELATION WITH retention_probability WITHIN ANOMALY-PRONE SEGMENTS (High Value, Standard, Basic) ===")
seg_mask = df['profitability_segment'].isin(['High Value','Standard','Basic'])
for f in ['comprehensive_customer_score','total_revenue','transaction_count','transaction_value_volatility',
          'seasonal_std','seasonal_max_share','seasonal_entropy','tx_ratio','score_rev_resid']:
    sub = df[seg_mask]
    r, p = stats.pearsonr(sub[f].dropna(), sub['retention_probability'][sub[f].notna()])
    rho, p_s = stats.spearmanr(sub[f].dropna(), sub['retention_probability'][sub[f].notna()])
    print(f"  {f:35s} Pearson r={r:+.3f} (p={p:.4f})   Spearman rho={rho:+.3f} (p={p_s:.4f})")

# ---- Regression: retention ~ score + revenue + tx + volatility + seasonal_std ----
print("\n=== REGRESSION: retention_probability ~ existing value metrics ===")
from numpy.linalg import lstsq
features = ['comprehensive_customer_score','total_revenue','transaction_count','transaction_value_volatility']
X = df[features].fillna(0).values
X = np.column_stack([np.ones(len(X)), X])
y = df['retention_probability'].values
coef, _, _, _ = lstsq(X, y, rcond=None)
y_pred = X @ coef
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res/ss_tot
print(f"  R^2 of retention ~ [score, revenue, tx_count, volatility] = {r2:.4f}")
print(f"  i.e. {100*(1-r2):.1f}% of retention variance is NOT explained by existing value metrics.")

# ---- Add new candidate dimensions ----
X2 = np.column_stack([np.ones(len(X)), df[features].fillna(0).values,
                      df['tx_ratio'].fillna(0).values, df['seasonal_std'].fillna(0).values])
coef2, _, _, _ = lstsq(X2, y, rcond=None)
y_pred2 = X2 @ coef2
ss_res2 = np.sum((y - y_pred2)**2)
r2_2 = 1 - ss_res2/ss_tot
print(f"  R^2 after adding [tx_ratio, seasonal_std] = {r2_2:.4f}  (delta = {r2_2-r2:+.4f})")

# ---- Key insight: retention in anomaly segments vs value metrics ----
print("\n=== AVERAGE RETENTION BY SEGMENT AND SCORE TERTILE ===")
df['score_bin'] = pd.qcut(df['comprehensive_customer_score'], 3, labels=['Low','Mid','High'])
tab = df.groupby(['profitability_segment','score_bin'])['retention_probability'].agg(['mean','count'])
print(tab.round(3).to_string())

# Save final
df.to_pickle('/work/df_final.pkl')
print("\nDone.")