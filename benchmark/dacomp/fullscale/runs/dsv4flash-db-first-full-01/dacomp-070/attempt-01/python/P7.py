import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load region×package data
df_rp = pd.read_csv('/work/region_package_monthly.csv')
df_rp['month_dt'] = pd.to_datetime(df_rp['month'] + '-01')
df_rp['month_num'] = (df_rp['month_dt'] - df_rp['month_dt'].min()).dt.days / 30.0
df_rp['conv_rate'] = 100.0 * df_rp['acquisitions'] / df_rp['visitors']

# =============================================
# 2. NON-LINEAR RELATIONSHIP ANALYSIS
# =============================================
print("=" * 60)
print("ANALYSIS 2: NON-LINEAR RELATIONSHIPS")
print("=" * 60)

# Quality vs Conversion Rate - check non-linearity
print("\n--- Quality Score vs Store Listing Conversion Rate ---")
print("Pearson correlation (linear):", df_rp['quality'].corr(df_rp['conv_rate']))

# Fit quadratic model: conv ~ quality + quality^2
x = df_rp['quality'].values
y = df_rp['conv_rate'].values
coeffs = np.polyfit(x, y, 2)
p = np.poly1d(coeffs)
print(f"Quadratic fit: conv = {coeffs[2]:.4f} + {coeffs[1]:.4f}*q + {coeffs[0]:.4f}*q^2")
y_pred = p(x)
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2_quad = 1 - ss_res/ss_tot
print(f"R-squared (quadratic): {r2_quad:.4f}")

# Linear fit for comparison
slope, intercept, r, p_lin, se = stats.linregress(x, y)
y_pred_lin = intercept + slope * x
ss_res_lin = np.sum((y - y_pred_lin)**2)
r2_lin = 1 - ss_res_lin/ss_tot
print(f"R-squared (linear): {r2_lin:.4f}")

# Test if quadratic is significantly better
# Using F-test for nested models
n = len(y)
f_stat = ((ss_res_lin - ss_res) / (2 - 1)) / (ss_res / (n - 3))
p_f = 1 - stats.f.cdf(f_stat, 1, n - 3)
print(f"F-stat for quadratic improvement: {f_stat:.4f}, p={p_f:.6f}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Quality vs Conversion
axes[0].scatter(x, y, alpha=0.5, c=df_rp['region'].astype('category').cat.codes, cmap='viridis')
x_sorted = np.sort(x)
axes[0].plot(x_sorted, p(x_sorted), 'r-', linewidth=2, label='Quadratic fit')
axes[0].plot(x_sorted, intercept + slope * x_sorted, 'b--', linewidth=2, label='Linear fit')
axes[0].set_xlabel('Quality Score')
axes[0].set_ylabel('Store Listing Conversion Rate (%)')
axes[0].set_title(f'Quality Score vs Conversion Rate\nQuadratic R²={r2_quad:.3f}, Linear R²={r2_lin:.3f}')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Crash Rate vs Conversion Rate
print("\n--- Crash Rate per 1k vs Store Listing Conversion Rate ---")
print("Pearson correlation (linear):", df_rp['crash'].corr(df_rp['conv_rate']))

x2 = df_rp['crash'].values
y2 = df_rp['conv_rate'].values
coeffs2 = np.polyfit(x2, y2, 2)
p2 = np.poly1d(coeffs2)
print(f"Quadratic fit: conv = {coeffs2[2]:.4f} + {coeffs2[1]:.4f}*c + {coeffs2[0]:.4f}*c^2")
y_pred2 = p2(x2)
ss_res2 = np.sum((y2 - y_pred2)**2)
ss_tot2 = np.sum((y2 - np.mean(y2))**2)
r2_quad2 = 1 - ss_res2/ss_tot2
print(f"R-squared (quadratic): {r2_quad2:.4f}")

slope2, intercept2, r2, p_lin2, se2 = stats.linregress(x2, y2)
y_pred_lin2 = intercept2 + slope2 * x2
ss_res_lin2 = np.sum((y2 - y_pred_lin2)**2)
r2_lin2 = 1 - ss_res_lin2/ss_tot2
print(f"R-squared (linear): {r2_lin2:.4f}")

# Log transform of crash rate
log_crash = np.log(df_rp['crash'].values + 0.001)  # avoid log(0)
slope_l, intercept_l, r_l, p_l, se_l = stats.linregress(log_crash, y2)
y_pred_log = intercept_l + slope_l * log_crash
ss_res_log = np.sum((y2 - y_pred_log)**2)
r2_log = 1 - ss_res_log/ss_tot2
print(f"R-squared (log(crash)): {r2_log:.4f}")

axes[1].scatter(x2, y2, alpha=0.5, c=df_rp['region'].astype('category').cat.codes, cmap='viridis')
x2_sorted = np.sort(x2)
axes[1].plot(x2_sorted, p2(x2_sorted), 'r-', linewidth=2, label='Quadratic fit')
axes[1].plot(x2_sorted, intercept2 + slope2 * x2_sorted, 'b--', linewidth=2, label='Linear fit')
axes[1].set_xlabel('Crash Rate per 1k')
axes[1].set_ylabel('Store Listing Conversion Rate (%)')
axes[1].set_title(f'Crash Rate vs Conversion Rate\nQuadratic R²={r2_quad2:.3f}, Linear R²={r2_lin2:.3f}')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig2_nonlinear_relationships.png', dpi=100)
plt.close()
print("Saved fig2_nonlinear_relationships.png")

# Joint non-linear model: conv ~ quality + quality^2 + log(crash)
print("\n--- Joint non-linear model ---")
X = np.column_stack([np.ones_like(x), x, x**2, np.log(df_rp['crash'].values + 0.001)])
beta = np.linalg.lstsq(X, y, rcond=None)[0]
y_pred_joint = X @ beta
ss_res_joint = np.sum((y - y_pred_joint)**2)
r2_joint = 1 - ss_res_joint/ss_tot
print(f"Joint model coefficients: {beta}")
print(f"Joint model R-squared: {r2_joint:.4f}")
print(f"Model: conv = {beta[0]:.4f} + {beta[1]:.4f}*q + {beta[2]:.4f}*q^2 + {beta[3]:.4f}*log(crash)")