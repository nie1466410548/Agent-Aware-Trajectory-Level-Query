import pandas as pd, numpy as np

df = pd.read_csv('/work/account_scored.csv')

# Let me try a different framing: 
# The "existing model" uses a simple formula: score = duration * frequency
# And high-value is defined by a separate process (e.g., actual revenue, which we approximate)
# Let's try defining high-value using a composite that excludes duration/frequency,
# and see what accuracy the 2D model gives

# Recompute dim (the percentile ranks)
def pct_rank(s):
    return s.rank(pct=True)

# Try: high-value = top 20% of a score that deliberately excludes duration/frequency
# This simulates a "true value" that comes from other dimensions
df['satisfaction'] = pct_rank(df['avg_nps_rating'])
df['adoption_score'] = (pct_rank(df['feature_click_ratio']) + pct_rank(df['page_view_ratio']) + pct_rank(df['active_visitor_ratio'])) / 3
df['breadth_score'] = (pct_rank(df['count_associated_visitors']) + pct_rank(df['count_active_visitors'])) / 2
df['diversity_score'] = (pct_rank(df['browser_diversity']) + pct_rank(df['os_diversity'])) / 2

# True value = satisfaction + breadth + adoption + diversity (NO duration/frequency)
df['true_value'] = (df['satisfaction'] * 0.25 + df['breadth_score'] * 0.25 + 
                    df['adoption_score'] * 0.25 + df['diversity_score'] * 0.25)
hv_thresh = df['true_value'].quantile(0.80)
df['hv_true'] = (df['true_value'] >= hv_thresh).astype(int)
print('True high-value (non-ENG):', df['hv_true'].sum())

# Existing model: uses only duration + frequency (linear combination)
df['dur_rank'] = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['freq_rank'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events']) + pct_rank(df['average_daily_events'])) / 3
# Try different weightings
for w_dur in [0.3, 0.5, 0.7]:
    df['old_score'] = df['dur_rank'] * w_dur + df['freq_rank'] * (1 - w_dur)
    # Match top 20% prediction rate
    old_thresh = df['old_score'].quantile(0.80)
    df['old_pred'] = (df['old_score'] >= old_thresh).astype(int)
    acc = (df['old_pred'] == df['hv_true']).mean()
    prec = df[(df['old_pred']==1)&(df['hv_true']==1)].shape[0] / max(df['old_pred'].sum(),1)
    rec = df[(df['old_pred']==1)&(df['hv_true']==1)].shape[0] / max(df['hv_true'].sum(),1)
    print(f'w_dur={w_dur}: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}')

# Now let's try: train a logistic regression on only 2 features 
# vs all features, using the true_value as ground truth
# Manual logistic regression
def standardize(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0) + 1e-8
    return (X - mu) / sd, mu, sd

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def logreg_fit(X, y, lr=0.3, iters=3000, l2=0.01):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    for i in range(iters):
        z = X @ w + b
        p = sigmoid(z)
        grad_w = (X.T @ (p - y)) / n + l2 * w
        grad_b = (p - y).mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b

def stratified_split(y, n_folds=5, seed=42):
    rng = np.random.RandomState(seed)
    idx = np.arange(len(y))
    folds = []
    classes = np.unique(y)
    for c in classes:
        c_idx = idx[y == c]
        rng.shuffle(c_idx)
        splits = np.array_split(c_idx, n_folds)
        for f in range(n_folds):
            if len(folds) <= f:
                folds.append([])
            folds[f].extend(splits[f].tolist())
    return [np.array(f) for f in folds]

def evaluate_cv(features, y, n_folds=5):
    X = features.astype(float)
    folds = stratified_split(y, n_folds)
    accs = []
    for f in range(n_folds):
        test_idx = folds[f]
        train_idx = np.concatenate([folds[g] for g in range(n_folds) if g != f])
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        Xtr_s, mu, sd = standardize(X_train)
        Xte_s = (X_test - mu) / sd
        w, b = logreg_fit(Xtr_s, y_train)
        proba = sigmoid(Xte_s @ w + b)
        y_pred = (proba >= 0.5).astype(int)
        acc = (y_pred == y_test).mean()
        accs.append(acc)
    return np.mean(accs), np.std(accs)

y = df['hv_true'].values

# 2D features
X_2d = df[['dur_rank', 'freq_rank']].values
acc_2d, std_2d = evaluate_cv(X_2d, y)
print(f'\n2D logistic regression CV: Acc={acc_2d:.4f} +/- {std_2d:.4f}')

# Multi-dim features
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
acc_multi, std_multi = evaluate_cv(X_multi, y)
print(f'Multi-dim logistic regression CV: Acc={acc_multi:.4f} +/- {std_multi:.4f}')

df.to_csv('/work/account_model.csv', index=False)
print('saved')