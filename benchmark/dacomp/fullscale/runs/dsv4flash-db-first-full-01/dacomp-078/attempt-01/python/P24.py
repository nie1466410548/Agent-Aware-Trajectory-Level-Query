import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi': 110, 'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})

# Figure 2: Model comparison - 2D vs multi-dimensional
df = pd.read_csv('/work/account_final_model.csv')
y = df['high_value'].values

# Redo CV to get metrics for both models (reproduce results)
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
    return np.mean(accs), np.mean(precs), np.mean(recs), np.mean(f1s)

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

r2d = cv_metrics(df[baseline_feats].values.astype(float), y)
rm = cv_metrics(df[multi_feats].values.astype(float), y)
print('2D:', np.round(r2d, 3), 'Multi:', np.round(rm, 3))

metrics = ['Accuracy', 'Precision', 'Recall', 'F1']
vals = np.array([r2d, rm])
x = np.arange(len(metrics)); width = 0.35
fig, ax = plt.subplots(figsize=(8, 5))
b1 = ax.bar(x - width/2, vals[0], width, label='Existing 2D model (duration + frequency)', color='#d1495b')
b2 = ax.bar(x + width/2, vals[1], width, label='New multi-dimensional model', color='#2e86ab')
for xi, (v1, v2) in enumerate(zip(vals[0], vals[1])):
    ax.text(xi - width/2, v1 + 0.01, f'{v1:.3f}', ha='center', fontsize=9)
    ax.text(xi + width/2, v2 + 0.01, f'{v2:.3f}', ha='center', fontsize=9)
ax.axhline(0.85, color='green', ls='--', lw=1.2)
ax.text(3.4, 0.855, '85% target', color='green', ha='right', fontsize=9)
ax.set_ylabel('Score')
ax.set_title('High-value customer identification: 5-fold CV comparison')
ax.set_xticks(x); ax.set_xticklabels(metrics)
ax.set_ylim(0, 1.08)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('figure2_model_comparison.png')
plt.close()
print('figure2 saved')