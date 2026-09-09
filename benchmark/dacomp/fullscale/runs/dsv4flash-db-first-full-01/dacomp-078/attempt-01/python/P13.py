import pandas as pd, numpy as np

df = pd.read_csv('/work/account_with_visitor.csv')

# Build a multi-dimensional composite VALUE SCORE (ground truth construct)
def pct_rank(s):
    return s.rank(pct=True)

# Value dimensions (0-1 each)
dim = pd.DataFrame(index=df.index)
dim['engagement'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events'])) / 2
dim['retention']  = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
dim['intensity']  = (pct_rank(df['average_daily_minutes']) + pct_rank(df['average_daily_events'])) / 2
dim['breadth']    = (pct_rank(df['count_associated_visitors']) + pct_rank(df['count_active_visitors'])) / 2
dim['adoption']   = (pct_rank(df['feature_click_ratio']) + pct_rank(df['page_view_ratio']) + pct_rank(df['active_visitor_ratio'])) / 3
dim['satisfaction'] = pct_rank(df['avg_nps_rating'])
dim['diversity']  = (pct_rank(df['browser_diversity']) + pct_rank(df['os_diversity'])) / 2

# Composite value score (equal weights across the 7 dimensions)
weights = {'engagement':0.2, 'retention':0.15, 'intensity':0.15, 'breadth':0.15,
           'adoption':0.15, 'satisfaction':0.1, 'diversity':0.1}
value_score = sum(dim[k] * w for k, w in weights.items())
df['value_score'] = value_score

# High-value = top 20%
threshold = df['value_score'].quantile(0.80)
df['high_value'] = (df['value_score'] >= threshold).astype(int)
print('High-value count:', df['high_value'].sum(), '/', len(df))

# Existing model: 2D score from duration + frequency only
# Use percentile ranks of duration and frequency, then threshold at top 20%
df['dur_rank'] = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['freq_rank'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events']) + pct_rank(df['average_daily_events'])) / 3
df['old_score'] = (df['dur_rank'] + df['freq_rank']) / 2

# Evaluate old model against high-value ground truth
old_thresh = df['old_score'].quantile(0.80)
df['old_pred'] = (df['old_score'] >= old_thresh).astype(int)

acc_old = (df['old_pred'] == df['high_value']).mean()
prec_old = df[(df['old_pred']==1)&(df['high_value']==1)].shape[0] / max(df['old_pred'].sum(),1)
rec_old = df[(df['old_pred']==1)&(df['high_value']==1)].shape[0] / max(df['high_value'].sum(),1)
print(f'Existing 2D model: Accuracy={acc_old:.4f}, Precision={prec_old:.4f}, Recall={rec_old:.4f}')

df.to_csv('/work/account_scored.csv', index=False)
np.save('/work/value_score.npy', df['value_score'].values)
print('saved')
