import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_pickle('/work/df_clustered.pkl')

def gini(y):
    if len(y) == 0:
        return 0
    p = np.mean(y)
    return 2 * p * (1 - p)

def best_split(X, y, min_samples_leaf=5):
    n = X.shape[0]
    best_gini = float('inf')
    best_feat = None
    best_thresh = None
    for j in range(X.shape[1]):
        sorted_idx = np.argsort(X[:, j])
        sorted_X = X[sorted_idx, j]
        sorted_y = y[sorted_idx]
        for i in range(len(sorted_X) - 1):
            if sorted_X[i] == sorted_X[i+1]:
                continue
            thresh = (sorted_X[i] + sorted_X[i+1]) / 2
            if (i+1) < min_samples_leaf or (n-i-1) < min_samples_leaf:
                continue
            g = (len(sorted_y[:i+1]) * gini(sorted_y[:i+1]) + len(sorted_y[i+1:]) * gini(sorted_y[i+1:])) / n
            if g < best_gini:
                best_gini = g
                best_feat = j
                best_thresh = thresh
    return best_feat, best_thresh, best_gini

def build_tree(X, y, feature_names, depth=0, max_depth=5, min_samples_leaf=5):
    n = len(y)
    if n < min_samples_leaf or depth >= max_depth or gini(y) < 0.01:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    feat_idx, thresh, gval = best_split(X, y, min_samples_leaf)
    if feat_idx is None:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    left_mask = X[:, feat_idx] <= thresh
    if left_mask.sum() < min_samples_leaf or (~left_mask).sum() < min_samples_leaf:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    left = build_tree(X[left_mask], y[left_mask], feature_names, depth+1, max_depth, min_samples_leaf)
    right = build_tree(X[~left_mask], y[~left_mask], feature_names, depth+1, max_depth, min_samples_leaf)
    return {'leaf': False, 'feature': feature_names[feat_idx], 'threshold': thresh,
            'gini': gval, 'left': left, 'right': right, 'count': n, 'depth': depth}

def print_tree(node, indent=''):
    if node['leaf']:
        print(f"{indent}[Leaf] anomaly_rate={node['prediction']:.3f}, n={node['count']}")
        return
    print(f"{indent}[{node['feature']} <= {node['threshold']:.3f}] gini={node['gini']:.3f}, n={node['count']}")
    print_tree(node['left'], indent + '  LEFT: ')
    print_tree(node['right'], indent + '  RIGHT:')

# Build dataset with numeric + one-hot categorical features
tree_features = ['transaction_value_volatility', 'tx_ratio', 'seasonal_std',
                 'seasonal_max_share', 'seasonal_entropy', 'score_rev_resid',
                 'comprehensive_customer_score', 'total_revenue', 'transaction_count',
                 'avg_transactions_per_month']
cat_features = ['seasonal_preference', 'transaction_consistency', 'lifecycle_stage',
                'activity_status', 'engagement_frequency', 'growth_potential', 'value_tier']

df_enc = pd.get_dummies(df[cat_features], prefix=cat_features)
X_n = df[tree_features].fillna(0).values
X_full = pd.concat([pd.DataFrame(X_n, columns=tree_features), df_enc], axis=1).fillna(0)
X_all = X_full.values
y = df['is_anomaly'].values

print("=== DECISION TREE WITH ALL FEATURES (numeric + categorical) ===")
tree_full = build_tree(X_all, y, list(X_full.columns), max_depth=5, min_samples_leaf=5)
print_tree(tree_full)

# Feature importance
def compute_importance(tree):
    imp = {}
    def traverse(node):
        if node['leaf']:
            return
        imp[node['feature']] = imp.get(node['feature'], 0) + node['gini'] * node['count']
        traverse(node['left']); traverse(node['right'])
    traverse(tree)
    total = sum(imp.values())
    return {k: v/total for k, v in sorted(imp.items(), key=lambda x: x[1], reverse=True)}

imp = compute_importance(tree_full)
print("\n=== FEATURE IMPORTANCE ===")
for k, v in list(imp.items())[:20]:
    print(f"  {k}: {v:.4f}")

# Out-of-bag accuracy assessment via simple cross-validation
from itertools import combinations
# Manual 5-fold CV for decision tree
def predict(tree, x):
    if tree['leaf']:
        return tree['prediction']
    if x[list(X_full.columns).index(tree['feature'])] <= tree['threshold']:
        return predict(tree['left'], x)
    else:
        return predict(tree['right'], x)

np.random.seed(42)
idx = np.random.permutation(len(y))
folds = np.array_split(idx, 5)
accs = []
aucs = []
for f in folds:
    train_idx = np.setdiff1d(np.arange(len(y)), f)
    tree_cv = build_tree(X_all[train_idx], y[train_idx], list(X_full.columns), max_depth=4, min_samples_leaf=5)
    preds = np.array([predict(tree_cv, X_all[i]) for i in f])
    acc = np.mean((preds > 0.5) == y[f])
    # simple AUC
    tp = np.sum((preds > 0.5) & (y[f] == 1))
    fp = np.sum((preds > 0.5) & (y[f] == 0))
    tn = np.sum((preds <= 0.5) & (y[f] == 0))
    fn = np.sum((preds <= 0.5) & (y[f] == 1))
    prec = tp/(tp+fp) if (tp+fp) > 0 else 0
    rec = tp/(tp+fn) if (tp+fn) > 0 else 0
    accs.append(acc)
    aucs.append((prec, rec))
print("\n=== 5-FOLD CV RESULTS (anomaly prediction) ===")
print(f"Accuracy per fold: {[round(a,3) for a in accs]}")
print(f"Mean accuracy: {np.mean(accs):.3f}")
print(f"Mean precision/recall: {tuple(np.round(np.mean(aucs, axis=0),3))}")

# Compare with baseline: predict majority class
print(f"Baseline (predict all non-anomaly): accuracy={np.mean(y==0):.3f}")

df.to_pickle('/work/df_final.pkl')
print("\nSaved df_final.pkl")