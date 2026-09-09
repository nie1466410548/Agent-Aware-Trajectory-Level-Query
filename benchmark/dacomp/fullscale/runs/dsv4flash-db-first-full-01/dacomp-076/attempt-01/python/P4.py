import pandas as pd, numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the full annotated dataset
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
print("Shape:", df.shape)
print("is_anomaly distribution:\n", df['is_anomaly'].value_counts())
print("profitability_segment distribution:\n", df['profitability_segment'].value_counts())
print("\nData types:\n", df.dtypes)

# Convert numeric columns
num_cols = ['total_revenue','net_profit','transaction_count','avg_transactions_per_month',
            'comprehensive_customer_score','retention_probability','transaction_value_volatility',
            'q1_transactions','q2_transactions','q3_transactions','q4_transactions','customer_age_days']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df['is_anomaly'] = df['is_anomaly'].astype(int)