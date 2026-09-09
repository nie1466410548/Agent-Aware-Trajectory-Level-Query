import pandas as pd, numpy as np

# Manual logistic regression (gradient descent) + stratified CV
def standardize(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0) + 1e-8
    return (X - mu) / sd, mu, sd

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def logreg_fit(X, y, lr=0.3, iters=3000, l2=0.01, verbose=False):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    prev_loss = None
    for i in range(iters):
        z = X @ w + b
        p = sigmoid(z)
        grad_w = (X.T @ (p - y)) / n + l2 * w
        grad_b = (p - y).mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b

def logreg_predict_proba(X, w, b):
    return sigmoid(X @ w + b)

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

def evaluate(y_true, y_prob, threshold=0.5):
    y_pred = (y_prob >= threshold).astype(int)
    acc = (y_pred == y_true).mean()
    tp = ((y_pred == 1) & (y_true == 1)).sum()
    fp = ((y_pred == 1) & (y_true == 0)).sum()
    fn = ((y_pred == 0) & (y_true == 1)).sum()
    tn = ((y_pred == 0) & (y_true == 0)).sum()
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    # AUC via rank
    n_pos = y_true.sum()
    n_neg = len(y_true) - n_pos
    if n_pos > 0 and n_neg > 0:
        order = np.argsort(y_prob)
        ranks = np.empty(len(y_true))
        ranks[order] = np.arange(1, len(y_true) + 1)
        auc = (ranks[y_true == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
    else:
        auc = np.nan
    return acc, prec, rec, f1, auc

df = pd.read_csv('/work/account_with_visitor.csv')
y = df['retained'].values

baseline_features = ['count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
                     'average_daily_minutes', 'average_daily_events']
multi_dim_features = [
    'count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    'avg_nps_rating',
    'browser_diversity', 'os_diversity',
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events'
]

def run_cv(features, y, n_folds=5, seed=42, threshold=0.5):
    X = df[features].values.astype(float)
    folds = stratified_split(y, n_folds, seed)
    results = []
    for f in range(n_folds):
        test_idx = folds[f]
        train_idx = np.concatenate([folds[g] for g in range(n_folds) if g != f])
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        Xtr_s, mu, sd = standardize(X_train)
        Xte_s = (X_test - mu) / sd
        w, b = logreg_fit(Xtr_s, y_train)
        proba = logreg_predict_proba(Xte_s, w, b)
        acc, prec, rec, f1, auc = evaluate(y_test, proba, threshold)
        results.append((acc, prec, rec, f1, auc))
    return np.array(results)

print('=== BASELINE (duration + frequency only) ===')
res_b = run_cv(baseline_features, y)
print('Acc: %.4f | Prec: %.4f | Rec: %.4f | F1: %.4f | AUC: %.4f' % tuple(res_b.mean(axis=0)))
print('Fold accs:', np.round(res_b[:, 0], 3))

print('\n=== MULTI-DIMENSIONAL MODEL ===')
res_m = run_cv(multi_dim_features, y)
print('Acc: %.4f | Prec: %.4f | Rec: %.4f | F1: %.4f | AUC: %.4f' % tuple(res_m.mean(axis=0)))
print('Fold accs:', np.round(res_m[:, 0], 3))

np.save('/work/baseline_results.npy', res_b)
np.save('/work/multidim_results.npy', res_m)
