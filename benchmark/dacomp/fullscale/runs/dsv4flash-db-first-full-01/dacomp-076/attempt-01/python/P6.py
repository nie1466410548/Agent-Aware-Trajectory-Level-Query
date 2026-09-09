import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_pickle('/work/df_full.pkl')

# ---- Group comparison: Anomaly vs Non-Anomaly ----
features = ['transaction_count','avg_transactions_per_month','transaction_value_volatility',
            'tx_ratio','tx_gap','seasonal_std','seasonal_max_share','seasonal_entropy',
            'seasonal_cv','comprehensive_customer_score','total_revenue','score_rev_resid',
            'rev_per_tx','profit_margin','retention_probability','customer_age_days']

print("=" * 90)
print("COMPARISON: ANOMALY vs NON-ANOMALY GROUPS")
print("=" * 90)
results = []
for f in features:
    g0 = df[df['is_anomaly']==0][f].dropna()
    g1 = df[df['is_anomaly']==1][f].dropna()
    m0, m1 = g0.mean(), g1.mean()
    std0, std1 = g0.std(), g1.std()
    # t-test
    t, p = stats.ttest_ind(g0, g1, equal_var=False)
    # cohens d
    d = (m1 - m0) / np.sqrt((std0**2 + std1**2)/2)
    results.append((f, m0, m1, std0, std1, t, p, d))
    
res_df = pd.DataFrame(results, columns=['Feature','NonAnomaly_Mean','Anomaly_Mean','NonAnomaly_Std','Anomaly_Std','t_stat','p_value','cohens_d'])
res_df['p_signif'] = res_df['p_value'].apply(lambda x: '***' if x<0.001 else ('**' if x<0.01 else ('*' if x<0.05 else '')))
print(res_df.round(4).to_string())
print()

# ---- Categorical feature comparison ----
cat_cols = ['profitability_segment','value_tier','lifecycle_stage','activity_status',
            'seasonal_preference','transaction_consistency','growth_potential',
            'engagement_frequency','recommended_action']
print("=" * 90)
print("CATEGORICAL DISTRIBUTIONS BY ANOMALY STATUS")
print("=" * 90)
for c in cat_cols:
    tab = pd.crosstab(df[c], df['is_anomaly'], normalize='columns').round(3)
    tab.columns = ['Non-Anomaly','Anomaly']
    print(f"\n{c}:")
    print(tab.to_string())