import pandas as pd, numpy as np

df = pd.read_csv('/work/account_model.csv')

# Reconstruct the full composite value score (all 7 dimensions, equal weights)
def pct_rank(s):
    return s.rank(pct=True)

df['engagement'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events'])) / 2
df['retention']  = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['intensity']  = (pct_rank(df['average_daily_minutes']) + pct_rank(df['average_daily_events'])) / 2
df['breadth']    = (pct_rank(df['count_associated_visitors']) + pct_rank(df['count_active_visitors'])) / 2
df['adoption']   = (pct_rank(df['feature_click_ratio']) + pct_rank(df['page_view_ratio']) + pct_rank(df['active_visitor_ratio'])) / 3
df['satisfaction'] = pct_rank(df['avg_nps_rating'])
df['diversity']  = (pct_rank(df['browser_diversity']) + pct_rank(df['os_diversity'])) / 2

weights = {'engagement':0.2, 'retention':0.15, 'intensity':0.15, 'breadth':0.15,
           'adoption':0.15, 'satisfaction':0.1, 'diversity':0.1}
df['value_score'] = sum(df[k] * w for k, w in weights.items())
hv_thresh = df['value_score'].quantile(0.80)
df['high_value'] = (df['value_score'] >= hv_thresh).astype(int)
print('High-value count:', df['high_value'].sum())

# 2D features for logistic regression
df['dur_rank'] = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['freq_rank'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events']) + pct_rank(df['average_daily_events'])) / 3

# Model functions
def standardize(X):
    mu = X.mean(axis=0); sd = X.std(axis=0) + 1e-8
    return (X - mu) / sd, mu, sd

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def logreg_fit(X, y, lr=0.3, iters=3000, l2=0.01):
    n, d = X.shape
    w = np.zeros(d); b = 0.0
    for i in range(iters):
        z = X @ w + b
        p = sigmoid(z)
        grad_w = (X.T @ (p - y)) / n + l2 * w
        grad_b = (p - y).mean()
        w -= lr * grad_w; b -= lr * grad_b
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

def evaluate_cv(X, y, n_folds=5, seed=42):
    folds = stratified_split(y, n_folds, seed)
    accs, precs, recs, f1s = [], [], [], []
    for f in range(n_folds):
        test_idx = folds[f]
        train_idx = np.concatenate([folds[g] for g in range(n_folds) if g != f])
        Xtr_s, mu, sd = standardize(X[train_idx])
        Xte_s = (X[test_idx] - mu) / sd
        w, b = logreg_fit(Xtr_s, y[train_idx])
        proba = sigmoid(Xte_s @ w + b)
        y_pred = (proba >= 0.5).astype(int)
        y_true = y[test_idx]
        acc = (y_pred == y_true).mean()
        tp = ((y_pred==1)&(y_true==1)).sum(); fp = ((y_pred==1)&(y_true==0)).sum()
        fn = ((y_pred==0)&(y_true==1)).sum()
        prec = tp/(tp+fp) if tp+fp>0 else 0
        rec = tp/(tp+fn) if tp+fn>0 else 0
        f1 = 2*prec*rec/(prec+rec) if prec+rec>0 else 0
        accs.append(acc); precs.append(prec); recs.append(rec); f1s.append(f1)
    return np.mean(accs), np.mean(precs), np.mean(recs), np.mean(f1s), accs

y = df['high_value'].values

# 2D model - use raw duration+frequency features
X_2d = df[['count_active_days','count_active_months','sum_minutes','sum_events','average_daily_minutes','average_daily_events']].values.astype(float)
res2 = evaluate_cv(X_2d, y)
print(f'2D model (duration+freq features): Acc={res2[0]:.4f} Prec={res2[1]:.4f} Rec={res2[2]:.4f} F1={res2[3]:.4f}')

# Multi-dim model
multi_feats = ['count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    'avg_nps_rating', 'browser_diversity', 'os_diversity',
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events']
X_multi = df[multi_feats].values.astype(float)
resm = evaluate_cv(X_multi, y)
print(f'Multi-dim model: Acc={resm[0]:.4f} Prec={resm[1]:.4f} Rec={resm[2]:.4f} F1={resm[3]:.4f}')

df.to_csv('/work/account_final_model.csv', index=False)
print('saved')