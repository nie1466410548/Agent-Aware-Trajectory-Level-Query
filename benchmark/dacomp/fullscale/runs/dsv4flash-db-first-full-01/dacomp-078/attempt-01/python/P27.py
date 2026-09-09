# Final accuracy comparison with proper statement
import pandas as pd, numpy as np

# Load the best model results
df = pd.read_csv('/work/account_final_model.csv')
y = df['high_value'].values

# Redo the 5-fold CV one more time to get clean metrics
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

def cv_metrics(X, y, threshold=0.5):
    folds = stratified_split(y, 5)
    accs, precs, recs, f1s = [], [], [], []
    for f in range(5):
        te = folds[f]; tr = np.concatenate([folds[g] for g in range(5) if g != f])
        Xtr_s, mu, sd = standardize(X[tr]); Xte_s = (X[te] - mu) / sd
        w, b = logreg_fit(Xtr_s, y[tr])
        proba = sigmoid(Xte_s @ w + b)
        pred = (proba >= threshold).astype(int)
        yt = y[te]
        acc = (pred == yt).mean()
        tp = ((pred==1)&(yt==1)).sum(); fp = ((pred==1)&(yt==0)).sum(); fn = ((pred==0)&(yt==1)).sum()
        prec = tp/(tp+fp) if tp+fp>0 else 0; rec = tp/(tp+fn) if tp+fn>0 else 0
        f1 = 2*prec*rec/(prec+rec) if prec+rec>0 else 0
        accs.append(acc); precs.append(prec); recs.append(rec); f1s.append(f1)
    return (np.mean(accs), np.mean(precs), np.mean(recs), np.mean(f1s)), (accs, precs, recs, f1s)

baseline_feats = ['count_active_days','count_active_months','sum_minutes','sum_events',
                  'average_daily_minutes','average_daily_events']
multi_feats = ['count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    'avg_nps_rating', 'browser_diversity', 'os_diversity',
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events']

r2d, _ = cv_metrics(df[baseline_feats].values.astype(float), y)
rm, _ = cv_metrics(df[multi_feats].values.astype(float), y)

print('=== FINAL RESULTS ===')
print(f'Baseline 2D model (duration + frequency):')
print(f'  Accuracy: {r2d[0]:.3f}  Precision: {r2d[1]:.3f}  Recall: {r2d[2]:.3f}  F1: {r2d[3]:.3f}')
print(f'Multi-dimensional model (26 features):')
print(f'  Accuracy: {rm[0]:.3f}  Precision: {rm[1]:.3f}  Recall: {rm[2]:.3f}  F1: {rm[3]:.3f}')
print(f'Accuracy improvement: +{rm[0]-r2d[0]:.1%}')
print(f'Recall improvement: +{rm[2]-r2d[2]:.1%}')
print(f'Target (85% accuracy): {"MET" if rm[0] >= 0.85 else "NOT MET"}')
print(f'Target (85% precision): {"MET" if rm[1] >= 0.85 else "NOT MET"}')

# Precision-recall for threshold tuning
print('\nMulti-dim model at different thresholds:')
for t in [0.3, 0.4, 0.5, 0.6, 0.7]:
    rm_t, _ = cv_metrics(df[multi_feats].values.astype(float), y, threshold=t)
    print(f'  threshold={t:.1f}: Acc={rm_t[0]:.3f} Prec={rm_t[1]:.3f} Rec={rm_t[2]:.3f}')