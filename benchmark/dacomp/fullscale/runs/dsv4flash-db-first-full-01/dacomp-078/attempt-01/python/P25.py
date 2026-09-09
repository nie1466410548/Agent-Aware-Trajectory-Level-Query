import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi': 110, 'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})

# Figure 3: Feature importance (top 12)
coef = pd.read_csv('/work/feature_importance.csv').sort_values('abs_coef', ascending=False).head(12)
fig, ax = plt.subplots(figsize=(8, 5.5))
colors = ['#2e86ab' if c > 0 else '#d1495b' for c in coef['coef']]
ax.barh(coef['feature'][::-1], coef['coef'][::-1], color=colors[::-1])
ax.set_xlabel('Standardized logistic regression coefficient')
ax.set_title('Multi-dimensional model: top feature contributions to high-value score')
plt.tight_layout()
plt.savefig('figure3_feature_importance.png')
plt.close()
print('figure3 saved')

# Figure 4: Retention rate by value-score decile (trend outlook)
df = pd.read_csv('/work/account_trend_outlook.csv')
df['decile'] = pd.qcut(df['value_score'], 10, labels=False)
ret_by_dec = df.groupby('decile')['retained'].mean()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(range(10), ret_by_dec.values, marker='o', color='#2e86ab')
ax.set_xlabel('Value-score decile (1 = lowest, 10 = highest)')
ax.set_ylabel('Share still active 3-6 months later')
ax.set_title('Value trend outlook: retention 3-6 months ahead by value score decile')
ax.set_ylim(0, 0.85)
for i, v in enumerate(ret_by_dec.values):
    ax.text(i, v + 0.02, f'{v:.0%}', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('figure4_retention_by_decile.png')
plt.close()
print('figure4 saved')