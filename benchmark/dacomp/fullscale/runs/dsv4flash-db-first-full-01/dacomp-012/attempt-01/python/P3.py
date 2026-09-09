import numpy as np, pandas as pd, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_json('/work/diamonds_analysis.json')

# Carat intervals
bins = [0, 0.5, 1.0, 1.5, df['carat'].max()]
labels = ['<=0.5 ct', '0.51-1.0 ct', '1.01-1.5 ct', '>1.5 ct']
df['interval'] = pd.cut(df['carat'], bins=bins, labels=labels, include_lowest=True)
df['ppc'] = df['price'] / df['carat']

sns.set_style('whitegrid')
sns.set_palette('Set2')

# Figure 1: Boxplot of price per carat by carat interval
fig1, ax1 = plt.subplots(figsize=(10, 6))
order = ['<=0.5 ct', '0.51-1.0 ct', '1.01-1.5 ct', '>1.5 ct']
sns.boxplot(data=df, x='interval', y='ppc', order=order, ax=ax1, 
            showfliers=False, width=0.6, palette='Set2')
# Add mean points
means = df.groupby('interval', observed=True)['ppc'].mean()
for i, lab in enumerate(order):
    ax1.scatter(i, means[lab], color='red', s=80, zorder=5, marker='D')
ax1.set_xlabel('Carat Interval')
ax1.set_ylabel('Price per Carat (USD)')
ax1.set_title('Figure 1: Price per Carat by Carat Interval\n(Diamonds = mean values)')
plt.tight_layout()
fig1.savefig('/work/fig1_ppc_by_interval.png', dpi=150)
print("Figure 1 saved")

# Figure 2: Fine-grained price per carat trend
df['carat_round'] = np.round(df['carat'] * 2) / 2  # 0.5 ct bins
fine_summary = df.groupby('carat_round').agg(n=('price','count'), avg_ppc=('ppc','mean')).reset_index()
fine_summary = fine_summary[fine_summary['n'] >= 50]

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(fine_summary['carat_round'], fine_summary['avg_ppc'], 'o-', color='#2c7bb6', markersize=4)
ax2.set_xlabel('Carat')
ax2.set_ylabel('Average Price per Carat (USD)')
ax2.set_title('Figure 2: Average Price per Carat by Carat (0.5 ct bins, ≥50 diamonds)')
ax2.grid(True, alpha=0.3)
plt.tight_layout()
fig2.savefig('/work/fig2_ppc_trend.png', dpi=150)
print("Figure 2 saved")

# Figure 3: Log-log scatter colored by clarity
fig3, ax3 = plt.subplots(figsize=(10, 7))
clarity_order = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
colors = plt.cm.viridis(np.linspace(0, 1, len(clarity_order)))
for i, cl in enumerate(clarity_order):
    sub = df[df['clarity'] == cl]
    ax3.scatter(sub['carat'], sub['price'], s=1, alpha=0.3, color=colors[i], label=cl, rasterized=True)
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlabel('Carat (log scale)')
ax3.set_ylabel('Price (USD, log scale)')
ax3.set_title('Figure 3: Price vs Carat by Clarity (log-log)')
ax3.legend(markerscale=5, title='Clarity', loc='lower right')
plt.tight_layout()
fig3.savefig('/work/fig3_loglog_clarity.png', dpi=150)
print("Figure 3 saved")

# Figure 4: Average ppc by clarity within carat intervals
fig4, ax4 = plt.subplots(figsize=(11, 6))
interval_order = ['<=0.5 ct', '0.51-1.0 ct', '1.01-1.5 ct', '>1.5 ct']
clarity_order_plot = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
cross = df.groupby(['interval', 'clarity'], observed=True)['ppc'].mean().unstack()
cross = cross[clarity_order_plot]
cross.plot(marker='o', ax=ax4, linewidth=2)
ax4.set_xlabel('Carat Interval')
ax4.set_ylabel('Average Price per Carat (USD)')
ax4.set_title('Figure 4: Price per Carat by Clarity within Carat Intervals')
ax4.legend(title='Clarity', bbox_to_anchor=(1.02, 1))
plt.tight_layout()
fig4.savefig('/work/fig4_clarity_by_interval.png', dpi=150)
print("Figure 4 saved")

# Figure 5: Average ppc by color within carat intervals
fig5, ax5 = plt.subplots(figsize=(11, 6))
color_order_plot = ['D','E','F','G','H','I','J']
cross_color = df.groupby(['interval', 'color'], observed=True)['ppc'].mean().unstack()
cross_color = cross_color[color_order_plot]
cross_color.plot(marker='o', ax=ax5, linewidth=2)
ax5.set_xlabel('Carat Interval')
ax5.set_ylabel('Average Price per Carat (USD)')
ax5.set_title('Figure 5: Price per Carat by Color within Carat Intervals')
ax5.legend(title='Color', bbox_to_anchor=(1.02, 1))
plt.tight_layout()
fig5.savefig('/work/fig5_color_by_interval.png', dpi=150)
print("Figure 5 saved")

# Figure 6: Regression coefficient bar chart (exp(coef))
coefs = pd.read_json('/work/regression_coefs.json')
fig6, axes = plt.subplots(1, 3, figsize=(16, 5))

# Cut coefficients
cut_coefs = coefs.loc[['cut_Good','cut_Very Good','cut_Premium','cut_Ideal'], 'exp_coef']
cut_coefs.index = ['Good','Very Good','Premium','Ideal']
axes[0].barh(cut_coefs.index, cut_coefs.values, color='steelblue')
axes[0].axvline(1.0, color='gray', linestyle='--')
axes[0].set_xlabel('Multiplier vs Fair')
axes[0].set_title('Cut Effect (vs Fair)')

# Color coefficients
color_coefs = coefs.loc[['color_I','color_H','color_G','color_F','color_E','color_D'], 'exp_coef']
color_coefs.index = ['I','H','G','F','E','D']
axes[1].barh(color_coefs.index, color_coefs.values, color='darkorange')
axes[1].axvline(1.0, color='gray', linestyle='--')
axes[1].set_xlabel('Multiplier vs J')
axes[1].set_title('Color Effect (vs J)')

# Clarity coefficients
clarity_coefs = coefs.loc[['clarity_SI2','clarity_SI1','clarity_VS2','clarity_VS1','clarity_VVS2','clarity_VVS1','clarity_IF'], 'exp_coef']
clarity_coefs.index = ['SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
axes[2].barh(clarity_coefs.index, clarity_coefs.values, color='forestgreen')
axes[2].axvline(1.0, color='gray', linestyle='--')
axes[2].set_xlabel('Multiplier vs I1')
axes[2].set_title('Clarity Effect (vs I1)')

plt.suptitle('Figure 6: Marginal Price Multipliers from Regression (log-log model, R²=0.98)', fontsize=14, y=1.02)
plt.tight_layout()
fig6.savefig('/work/fig6_regression_multipliers.png', dpi=150, bbox_inches='tight')
print("Figure 6 saved")

# Summary stats text
summary = df.groupby('interval', observed=True).agg(
    n=('price','count'),
    avg_carat=('carat','mean'),
    avg_price=('price','mean'),
    avg_ppc=('ppc','mean'),
    median_ppc=('ppc','median'),
    sd_ppc=('ppc','std')
).round(2)
print("\n=== Summary by Carat Interval ===")
print(summary.to_string())

# Also compute avg ppc by cut within interval
cut_ppc = df.groupby(['interval', 'cut'], observed=True)['ppc'].mean().unstack()
print("\n=== Avg PPC by Cut within Interval ===")
print(cut_ppc.round(2).to_string())

color_ppc = df.groupby(['interval', 'color'], observed=True)['ppc'].mean().unstack()
print("\n=== Avg PPC by Color within Interval ===")
print(color_ppc.round(2).to_string())

clarity_ppc = df.groupby(['interval', 'clarity'], observed=True)['ppc'].mean().unstack()
print("\n=== Avg PPC by Clarity within Interval ===")
print(clarity_ppc.round(2).to_string())