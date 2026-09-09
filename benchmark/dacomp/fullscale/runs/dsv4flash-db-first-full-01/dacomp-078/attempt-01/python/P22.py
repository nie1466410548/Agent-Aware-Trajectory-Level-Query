import pandas as pd, numpy as np

df = pd.read_csv('/work/account_final_model.csv')

# How well does the multi-dimensional value score predict the FUTURE retention outcome?
# retention = still active after July 1 (i.e., value trend holds over the next 3-6 months)
# Note: value_score is computed from full-period features; retention is the temporal outcome.
# We use correlation and AUC-like separation as descriptive evidence.
df['retained'] = (pd.to_datetime(df['last_event_on']) >= '2024-07-01').astype(int)

# Rank-based separation
def auc(y_true, scores):
    n_pos = y_true.sum(); n_neg = len(y_true) - n_pos
    order = np.argsort(scores)
    ranks = np.empty(len(scores)); ranks[order] = np.arange(1, len(scores)+1)
    return (ranks[y_true==1].sum() - n_pos*(n_pos+1)/2) / (n_pos*n_neg)

auc_val = auc(df['retained'].values, df['value_score'].values)
corr = df['value_score'].corr(df['retained'])
print(f'Correlation value_score vs retention: {corr:.4f}')
print(f'AUC of value_score for predicting retention: {auc_val:.4f}')

# Retention rate by value score decile
df['decile'] = pd.qcut(df['value_score'], 10, labels=False)
print('\nRetention rate by value-score decile:')
print(df.groupby('decile')['retained'].mean().round(3).to_string())

# Trend outlook classification:
# "stable/growing" if retained==1 (value continues into the next 3-6 months)
# Predict via logistic regression on multi-dim features, evaluate CV accuracy
def standardize(X):
    mu = X.mean(axis=0); sd = X.std(axis=0) + 1e-8
    return (X - mu) / sd, mu, sd

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def logreg_fit(X, y, lr=0.3, iters=4000, l2=0.01):
    n, d = X.shape
    w = np.zeros(d); b = 0.0
    for i in range(iters):
        z = X @ w + b
        p = sigmoid(z)
        gw = (X.T @ (p - y)) / n + l2 * w
        gb = (p - y).mean()
        w -= lr * gw; b -= lr * gb
    return w, b

def stratified_split(y, n_folds=5, seed=42):
    rng = np.random.RandomState(seed)
    idx = np.arange(len(y)); folds = []
    for c in np.unique(y):
        c_idx = idx[y == c]; rng.shuffle(c_idx)
        for f, sp in enumerate(np.array_split(c_idx, n_folds)):
            if len(folds) <= f: folds.append([])
            folds[f].extend(sp.tolist())
    return [np.array(f) for f in folds]

multi_feats = ['count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    'avg_nps_rating', 'browser_diversity', 'os_diversity',
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events']

y = df['retained'].values
X = df[multi_feats].values.astype(float)
folds = stratified_split(y, 5)
accs = []
for f in range(5):
    te = folds[f]; tr = np.concatenate([folds[g] for g in range(5) if g != f])
    Xtr_s, mu, sd = standardize(X[tr]); Xte_s = (X[te] - mu) / sd
    w, b = logreg_fit(Xtr_s, y[tr])
    proba = sigmoid(Xte_s @ w + b)
    pred = (proba >= 0.5).astype(int)
    accs.append((pred == y[te]).mean())
print(f'\nValue-trend outlook model (retention prediction) CV accuracy: {np.mean(accs):.4f} +/- {np.std(accs):.4f}')
print('Fold accs:', np.round(accs, 3))

df.to_csv('/work/account_trend_outlook.csv', index=False)
print('saved')