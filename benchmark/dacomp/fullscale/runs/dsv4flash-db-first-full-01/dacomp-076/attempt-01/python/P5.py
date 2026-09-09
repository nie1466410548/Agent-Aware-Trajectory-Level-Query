import pandas as pd, numpy as np, json, os
from scipy import stats

path = '/results/S20.rows.jsonl'
rows = []
with open(path) as f:
    for line in f:
        rows.append(json.loads(line))
cols = ['customer_id','customer_name','customer_email','subsidiary_id','profitability_segment',
        'value_tier','lifecycle_stage','activity_status','retention_category','total_revenue',
        'net_profit','transaction_count','avg_transactions_per_month','comprehensive_customer_score',
        'retention_probability','seasonal_preference','transaction_consistency','growth_potential',
        'recommended_action','engagement_frequency','customer_age_days','segmentation_date',
        'transaction_value_volatility','q1_transactions','q2_transactions','q3_transactions',
        'q4_transactions','customer_analytics_id','avg_retention','deviation','is_anomaly','is_above_avg']
df = pd.DataFrame(rows, columns=cols)
num_cols = ['total_revenue','net_profit','transaction_count','avg_transactions_per_month',
            'comprehensive_customer_score','retention_probability','transaction_value_volatility',
            'q1_transactions','q2_transactions','q3_transactions','q4_transactions','customer_age_days']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df['is_anomaly'] = df['is_anomaly'].astype(int)

# ---- Transactional behavior features ----
# Expected transactions over observed age (365 days ~ 12 months)
df['months'] = df['customer_age_days'] / 30.44
df['expected_tx'] = df['avg_transactions_per_month'] * df['months']
df['tx_ratio'] = df['transaction_count'] / df['expected_tx']  # >1 means more tx than monthly avg implies
df['tx_gap'] = df['transaction_count'] - df['expected_tx']

# ---- Seasonal features ----
qcols = ['q1_transactions','q2_transactions','q3_transactions','q4_transactions']
df['seasonal_total'] = df[qcols].sum(axis=1)
qshares = df[qcols].div(df['seasonal_total'].replace(0, np.nan), axis=0)
df['seasonal_std'] = qshares.std(axis=1)          # concentration: higher = unbalanced
df['seasonal_max_share'] = qshares.max(axis=1)    # max quarter share
df['seasonal_cv'] = df['seasonal_std'] / (1/2)    # normalized std vs uniform 0.25
# entropy-based balance
eps = 1e-9
df['seasonal_entropy'] = -(qshares * np.log(qshares + eps)).sum(axis=1) / np.log(4)  # 1 = perfectly balanced

# dominant quarter
df['dominant_q'] = qshares.idxmax(axis=1).str.replace('q','Q').str.replace('_transactions',' Peak')

# ---- Value realization alignment ----
# Regress comprehensive_customer_score on total_revenue -> residual indicates score not explained by revenue
slope, intercept, r, p, se = stats.linregress(df['total_revenue'], df['comprehensive_customer_score'])
df['score_rev_resid'] = df['comprehensive_customer_score'] - (intercept + slope*df['total_revenue'])
# Also normalize: score relative to segment/revenue expectations
df['rev_per_tx'] = df['total_revenue'] / df['transaction_count'].replace(0, np.nan)
df['profit_margin'] = df['net_profit'] / df['total_revenue'].replace(0, np.nan)

print("Derived feature summary:")
print(df[['tx_ratio','tx_gap','seasonal_std','seasonal_max_share','seasonal_entropy','seasonal_cv','score_rev_resid','rev_per_tx']].describe().T)

# Save for reuse
df.to_pickle('/work/df_full.pkl')
print("\nSaved.")