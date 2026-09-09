import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_pickle('/work/df_full.pkl')

# ---- K-Means Clustering (manual implementation since sklearn unavailable) ----
def kmeans(X, k, max_iter=100, n_init=10, random_state=42):
    best_inertia = np.inf
    best_labels = None
    best_centers = None
    n = X.shape[0]
    for init in range(n_init):
        np.random.seed(random_state + init)
        # Smart initialization: pick random points
        idx = np.random.choice(n, k, replace=False)
        centers = X[idx].copy()
        for _ in range(max_iter):
            # Assign
            dists = np.sqrt(((X[:, None] - centers[None, :])**2).sum(axis=2))
            labels = np.argmin(dists, axis=1)
            # Update centers
            new_centers = np.array([X[labels == i].mean(axis=0) if (labels == i).sum() > 0 else centers[i] for i in range(k)])
            # Check convergence
            if np.allclose(centers, new_centers, atol=1e-8):
                break
            centers = new_centers
        # Compute inertia
        inertia = sum(((X[labels == i] - centers[i])**2).sum() for i in range(k))
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels
            best_centers = centers
    return best_labels, best_centers, best_inertia

# Select features for clustering
cluster_features = ['transaction_value_volatility', 'tx_ratio', 'seasonal_std', 
                    'score_rev_resid', 'comprehensive_customer_score', 'total_revenue',
                    'transaction_count']
X = df[cluster_features].fillna(0).values

# Standardize
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_std[X_std == 0] = 1
X_scaled = (X - X_mean) / X_std

# Find optimal k using elbow method
inertias = []
for k in range(2, 9):
    labels, centers, inertia = kmeans(X_scaled, k, random_state=42)
    inertias.append(inertia)
    print(f"k={k}, inertia={inertia:.2f}")

# Plot elbow curve
plt.figure(figsize=(8, 5))
plt.plot(range(2, 9), inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of clusters (k)', fontsize=12)
plt.ylabel('Inertia (within-cluster sum of squares)', fontsize=12)
plt.title('Elbow Method for Optimal k', fontsize=13)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/elbow_curve.png')
plt.close()

# Run clustering with k=4 (elbow suggests k=3 or k=4)
k_optimal = 4
labels, centers, _ = kmeans(X_scaled, k_optimal, random_state=42)
df['cluster'] = labels

# Silhouette score (manual)
def silhouette_score(X, labels):
    n = X.shape[0]
    k = len(np.unique(labels))
    s = np.zeros(n)
    for i in range(n):
        a = np.mean(np.sqrt(((X[labels == labels[i]] - X[i])**2).sum(axis=1)))
        b_vals = []
        for j in range(k):
            if j == labels[i]:
                continue
            b_vals.append(np.mean(np.sqrt(((X[labels == j] - X[i])**2).sum(axis=1))))
        b = min(b_vals) if b_vals else 0
        s[i] = (b - a) / max(a, b)
    return np.mean(s)

sil = silhouette_score(X_scaled, labels)
print(f"\nSilhouette score (k={k_optimal}): {sil:.4f}")

# Cluster characteristics
print("\n--- Cluster Characteristics ---")
for clust in range(k_optimal):
    mask = df['cluster'] == clust
    print(f"\nCluster {clust} (n={mask.sum()}):")
    for f in cluster_features:
        print(f"  {f}: mean={df.loc[mask, f].mean():.3f}, std={df.loc[mask, f].std():.3f}")
    print(f"  is_anomaly: {df.loc[mask, 'is_anomaly'].mean():.3f}")
    print(f"  profitability_segment: {df.loc[mask, 'profitability_segment'].value_counts().to_dict()}")
    print(f"  lifecycle_stage: {df.loc[mask, 'lifecycle_stage'].value_counts().to_dict()}")
    print(f"  seasonal_preference: {df.loc[mask, 'seasonal_preference'].value_counts().to_dict()}")
    print(f"  transaction_consistency: {df.loc[mask, 'transaction_consistency'].value_counts().to_dict()}")

# Save cluster data
df.to_pickle('/work/df_clustered.pkl')

# Cluster visualization (2D PCA)
from numpy.linalg import svd
U, s, Vt = svd(X_scaled, full_matrices=False)
X_pca = U[:, :2] * s[:2]

plt.figure(figsize=(10, 7))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', s=60, alpha=0.7, edgecolors='k')
plt.colorbar(scatter, label='Cluster')
plt.xlabel('PC1', fontsize=12)
plt.ylabel('PC2', fontsize=12)
plt.title(f'K-Means Clusters (k={k_optimal}) in PCA Space', fontsize=13)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/clusters_pca.png')
plt.close()

# Anomaly overlay
plt.figure(figsize=(10, 7))
colors = ['blue' if a == 0 else 'red' for a in df['is_anomaly']]
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=colors, s=60, alpha=0.7, edgecolors='k')
plt.xlabel('PC1', fontsize=12)
plt.ylabel('PC2', fontsize=12)
plt.title('Anomaly (red) vs Non-Anomaly (blue) in PCA Space', fontsize=13)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/anomaly_pca.png')
plt.close()

print("\nDone. Figures saved.")
print("\nCluster cross-tab with anomaly status:")
print(pd.crosstab(df['cluster'], df['is_anomaly'], margins=True))
print("\nCluster cross-tab with segment:")
print(pd.crosstab(df['cluster'], df['profitability_segment'], margins=True))