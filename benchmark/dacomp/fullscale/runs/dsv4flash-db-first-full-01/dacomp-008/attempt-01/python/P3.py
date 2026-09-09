import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/project_data.csv')

# ---- Kruskal-Wallis tests ----
# 1. Deviation by Project Type (all projects)
groups = [g['deviation'].values for _, g in df.groupby('Project Type')]
h, p = stats.kruskal(*groups)
print(f"Kruskal-Wallis: deviation by Project Type (all)")
print(f"  H={h:.4f}, p={p:.6f}")

# 2. Deviation by Project Type (completed only)
df_comp = df[df['status'] == 'Completed']
groups_comp = [g['deviation'].values for _, g in df_comp.groupby('Project Type')]
h2, p2 = stats.kruskal(*groups_comp)
print(f"Kruskal-Wallis: deviation by Project Type (completed)")
print(f"  H={h2:.4f}, p={p2:.6f}")

# 3. Deviation by Risk Level (all)
groups_risk = [g['deviation'].values for _, g in df.groupby('risk')]
h3, p3 = stats.kruskal(*groups_risk)
print(f"Kruskal-Wallis: deviation by Risk Level (all)")
print(f"  H={h3:.4f}, p={p3:.6f}")

# 4. Deviation by Risk Level (completed)
groups_risk_comp = [g['deviation'].values for _, g in df_comp.groupby('risk')]
h4, p4 = stats.kruskal(*groups_risk_comp)
print(f"Kruskal-Wallis: deviation by Risk Level (completed)")
print(f"  H={h4:.4f}, p={p4:.6f}")

# 5. Deviation by Priority (all)
groups_pri = [g['deviation'].values for _, g in df.groupby('Priority')]
h5, p5 = stats.kruskal(*groups_pri)
print(f"Kruskal-Wallis: deviation by Priority (all)")
print(f"  H={h5:.4f}, p={p5:.6f}")

# 6. Deviation by Status
groups_st = [g['deviation'].values for _, g in df.groupby('status')]
h6, p6 = stats.kruskal(*groups_st)
print(f"Kruskal-Wallis: deviation by Status")
print(f"  H={h6:.4f}, p={p6:.6f}")

# ---- Spearman correlations (non-parametric) ----
from scipy.stats import spearmanr

# Overall
print("\n--- Spearman Correlations (All Projects) ---")
for col in ['team', 'sat', 'budget', 'actual']:
    r, p = spearmanr(df['deviation'], df[col])
    print(f"  deviation vs {col}: rho={r:.4f}, p={p:.6f}")

# Completed only
print("\n--- Spearman Correlations (Completed Projects) ---")
for col in ['team', 'sat', 'budget', 'actual']:
    r, p = spearmanr(df_comp['deviation'], df_comp[col])
    print(f"  deviation vs {col}: rho={r:.4f}, p={p:.6f}")

# Deviation percentage correlations
print("\n--- Spearman Correlations: dev_pct vs factors (All) ---")
for col in ['team', 'sat', 'budget']:
    r, p = spearmanr(df['dev_pct'], df[col])
    print(f"  dev_pct vs {col}: rho={r:.4f}, p={p:.6f}")

print("\n--- Spearman Correlations: dev_pct vs factors (Completed) ---")
for col in ['team', 'sat', 'budget']:
    r, p = spearmanr(df_comp['dev_pct'], df_comp[col])
    print(f"  dev_pct vs {col}: rho={r:.4f}, p={p:.6f}")

# Mean deviation by project type and risk
print("\n--- Summary Stats by Project Type & Risk ---")
summary = df.groupby(['Project Type', 'risk']).agg(
    n=('deviation', 'count'),
    mean_dev=('deviation', 'mean'),
    std_dev=('deviation', 'std'),
    median_dev=('deviation', 'median'),
    mean_dev_pct=('dev_pct', 'mean')
).round(2)
print(summary.to_string())

print("\n--- Summary Stats by Project Type & Status ---")
summary2 = df.groupby(['Project Type', 'status']).agg(
    n=('deviation', 'count'),
    mean_dev=('deviation', 'mean'),
    median_dev=('deviation', 'median')
).round(2)
print(summary2.to_string())