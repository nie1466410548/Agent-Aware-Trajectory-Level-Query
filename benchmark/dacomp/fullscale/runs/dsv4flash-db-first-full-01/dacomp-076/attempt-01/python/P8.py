import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_pickle('/work/df_clustered.pkl')

# ---- Decision Tree (CART-like) ----
# Implement a simple recursive binary split for classification

def gini(y):
    """Gini impurity"""
    if len(y) == 0:
        return 0
    p = np.mean(y)
    return 2 * p * (1 - p)  # for binary

def best_split(X, y, feature_names, min_samples_leaf=5):
    n, m = X.shape
    best_gini = float('inf')
    best_feat = None
    best_thresh = None
    parent_gini = gini(y)
    
    for j in range(m):
        # Get unique sorted values
        sorted_idx = np.argsort(X[:, j])
        sorted_X = X[sorted_idx, j]
        sorted_y = y[sorted_idx]
        
        for i in range(len(sorted_X) - 1):
            if sorted_X[i] == sorted_X[i+1]:
                continue
            thresh = (sorted_X[i] + sorted_X[i+1]) / 2
            left_y = sorted_y[:i+1]
            right_y = sorted_y[i+1:]
            if len(left_y) < min_samples_leaf or len(right_y) < min_samples_leaf:
                continue
            # Weighted gini
            g = (len(left_y) * gini(left_y) + len(right_y) * gini(right_y)) / n
            if g < best_gini:
                best_gini = g
                best_feat = j
                best_thresh = thresh
    return best_feat, best_thresh, best_gini

def build_tree(X, y, feature_names, depth=0, max_depth=5, min_samples_leaf=5):
    n = len(y)
    if n < min_samples_leaf or depth >= max_depth or gini(y) < 0.01:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    
    feat_idx, thresh, gini_val = best_split(X, y, feature_names, min_samples_leaf)
    if feat_idx is None:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    
    left_mask = X[:, feat_idx] <= thresh
    right_mask = ~left_mask
    
    if left_mask.sum() < min_samples_leaf or right_mask.sum() < min_samples_leaf:
        return {'leaf': True, 'prediction': np.mean(y), 'count': n, 'depth': depth}
    
    left_tree = build_tree(X[left_mask], y[left_mask], feature_names, depth+1, max_depth, min_samples_leaf)
    right_tree = build_tree(X[right_mask], y[right_mask], feature_names, depth+1, max_depth, min_samples_leaf)
    
    return {
        'leaf': False,
        'feature': feature_names[feat_idx],
        'threshold': thresh,
        'gini': gini_val,
        'left': left_tree,
        'right': right_tree,
        'count': n,
        'depth': depth
    }

def print_tree(node, indent=''):
    if node['leaf']:
        print(f"{indent}[Leaf] pred={node['prediction']:.3f}, n={node['count']}")
        return
    print(f"{indent}[{node['feature']} <= {node['threshold']:.3f}] (gini={node['gini']:.3f}, n={node['count']})")
    print(f"{indent}  LEFT:")
    print_tree(node['left'], indent + '    ')
    print(f"{indent}  RIGHT:")
    print_tree(node['right'], indent + '    ')

# Prepare features for decision tree
tree_features = ['transaction_value_volatility', 'tx_ratio', 'seasonal_std', 
                 'seasonal_max_share', 'seasonal_entropy', 'score_rev_resid',
                 'comprehensive_customer_score', 'total_revenue', 'transaction_count',
                 'avg_transactions_per_month']
X_tree = df[tree_features].fillna(0).values
y_tree = df['is_anomaly'].values

# Build tree
print("=== DECISION TREE FOR ANOMALY PREDICTION ===")
tree = build_tree(X_tree, y_tree, tree_features, max_depth=4, min_samples_leaf=5)
print_tree(tree)

# Also add categorical features via one-hot encoding for better tree
from sklearn.preprocessing import OneHotEncoder
# Actually sklearn is not available... Let me do manual one-hot
cat_features = ['seasonal_preference', 'transaction_consistency', 'lifecycle_stage', 
                'activity_status', 'engagement_frequency', 'growth_potential']

tree_features2 = tree_features + cat_features
# For categorical, we need to encode them. Let me do label encoding for simplicity
from sklearn.preprocessing import LabelEncoder
# Actually sklearn is not available. Let me use pandas get_dummies
df_encoded = pd.get_dummies(df[cat_features], prefix=cat_features, drop_first=False)
X_tree2 = pd.concat([pd.DataFrame(X_tree, columns=tree_features), df_encoded], axis=1).fillna(0).values
tree_features2_names = list(tree_features) + list(df_encoded.columns)

print(f"\n\n=== DECISION TREE WITH CATEGORICAL FEATURES ({len(tree_features2_names)} features) ===")
tree2 = build_tree(X_tree2, y_tree, tree_features2_names, max_depth=4, min_samples_leaf=5)
print_tree(tree2)

# Also try a simpler tree with just the key dimensions
print("\n\n=== KEY FINDINGS SUMMARY ===")
# Count anomaly rate by each dimension
for col in ['profitability_segment', 'lifecycle_stage', 'seasonal_preference', 
            'transaction_consistency', 'activity_status', 'engagement_frequency']:
    print(f"\nAnomaly rate by {col}:")
    rates = df.groupby(col)['is_anomaly'].agg(['mean', 'count'])
    print(rates.round(3).to_string())

# Feature importance based on gini reduction
def compute_importance(tree, feature_names):
    imp = {f: 0.0 for f in feature_names}
    def traverse(node, n_parent):
        if node['leaf']:
            return
        imp[node['feature']] += node['gini'] * node['count']
        traverse(node['left'], node['count'])
        traverse(node['right'], node['count'])
    traverse(tree, tree['count'])
    # Normalize
    total = sum(imp.values())
    if total > 0:
        for k in imp:
            imp[k] /= total
    return imp

imp = compute_importance(tree2, tree_features2_names)
top_imp = sorted(imp.items(), key=lambda x: x[1], reverse=True)
print("\n\n=== FEATURE IMPORTANCE (from decision tree) ===")
for feat, val in top_imp[:15]:
    print(f"  {feat}: {val:.4f}")

# Save
df.to_pickle('/work/df_final.pkl')
print("\nDone.")