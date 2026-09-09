import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('work/sheet1_full.csv')

# Figure 1: Trend shape - scatter + group means with LOESS-like smooth
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left: scatter + group means + linear fit
ax = axes[0]
ax.scatter(df['Mental health score'], df['Exam score'], alpha=0.2, s=10, c='gray', label='Data')
gm = df.groupby('Mental health score')['Exam score'].agg(['mean', 'std', 'count'])
x = gm.index.values
y = gm['mean'].values
ci = 1.96 * gm['std'] / np.sqrt(gm['count'])
ax.errorbar(x, y, yerr=ci, fmt='o-', color='#e63946', linewidth=2, capsize=4, label='Mean ± 95% CI')
# Linear fit line
from scipy import stats
slope, intercept, r_val, p_val, se = stats.linregress(df['Mental health score'], df['Exam score'])
x_line = np.linspace(0.5, 10.5, 100)
ax.plot(x_line, intercept + slope*x_line, '--', color='#457b9d', linewidth=2, label=f'Linear fit (R²={r_val**2:.3f})')
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Exam score', fontsize=12)
ax.set_title('A: Mental Health vs Exam Score', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.set_xlim(0.5, 10.5)

# Right: smooth cubic fit + group means
ax = axes[1]
ax.scatter(df['Mental health score'], df['Exam score'], alpha=0.15, s=8, c='gray', label='Data')
ax.errorbar(x, y, yerr=ci, fmt='o', color='#e63946', capsize=4, markersize=6, label='Group mean')
# Cubic fit
coef3 = np.polyfit(df['Mental health score'], df['Exam score'], 3)
x_smooth = np.linspace(1, 10, 200)
y_smooth = np.polyval(coef3, x_smooth)
ax.plot(x_smooth, y_smooth, '-', color='#2a9d8f', linewidth=2, label='Cubic smooth')
# Also show where the slope changes most
# compute derivative
dydx = 3*coef3[0]*x_smooth**2 + 2*coef3[1]*x_smooth + coef3[2]
# inflection where 2nd derivative=0
inflection = -coef3[1]/(3*coef3[0])  # 2nd derivative = 6a*x + 2b = 0 => x = -b/(3a)
if 1 <= inflection <= 10:
    ax.axvline(inflection, color='orange', ls=':', lw=1.5, alpha=0.7, label=f'Inflection ≈ {inflection:.1f}')
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Exam score', fontsize=12)
ax.set_title('B: Cubic smooth with inflection point', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.set_xlim(0.5, 10.5)

plt.tight_layout()
plt.savefig('work/fig1_trend.png', dpi=150)
plt.close()
print("Figure 1 saved")