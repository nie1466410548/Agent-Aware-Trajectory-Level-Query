import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_pickle('/work/df_final.pkl')

# Set style
sns.set_style("whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

# FIGURE 1: Anomaly rate by segment
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
sns.barplot(x='profitability_segment', y='is_anomaly', data=df, ax=axes[0,0], 
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[0,0].set_title('Anomaly Rate by Profitability Segment', fontsize=12)
axes[0,0].set_ylabel('% Anomaly')
axes[0,0].set_xlabel('')

sns.barplot(x='lifecycle_stage', y='is_anomaly', data=df, ax=axes[0,1],
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[0,1].set_title('Anomaly Rate by Lifecycle Stage', fontsize=12)
axes[0,1].set_ylabel('% Anomaly')
axes[0,1].set_xlabel('')

sns.barplot(x='seasonal_preference', y='is_anomaly', data=df, ax=axes[0,2],
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[0,2].set_title('Anomaly Rate by Seasonal Preference', fontsize=12)
axes[0,2].set_ylabel('% Anomaly')
axes[0,2].set_xlabel('')

sns.barplot(x='transaction_consistency', y='is_anomaly', data=df, ax=axes[1,0],
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[1,0].set_title('Anomaly Rate by Transaction Consistency', fontsize=12)
axes[1,0].set_ylabel('% Anomaly')
axes[1,0].set_xlabel('')

sns.barplot(x='activity_status', y='is_anomaly', data=df, ax=axes[1,1],
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[1,1].set_title('Anomaly Rate by Activity Status', fontsize=12)
axes[1,1].set_ylabel('% Anomaly')
axes[1,1].set_xlabel('')

sns.barplot(x='engagement_frequency', y='is_anomaly', data=df, ax=axes[1,2],
            palette='Set2', estimator=lambda x: np.mean(x)*100)
axes[1,2].set_title('Anomaly Rate by Engagement Frequency', fontsize=12)
axes[1,2].set_ylabel('% Anomaly')
axes[1,2].set_xlabel('')

plt.tight_layout()
plt.savefig('/work/anomaly_by_dimension.png', dpi=150)
plt.close()

# FIGURE 2: Seasonal distribution comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# Anomaly vs non-anomaly seasonal concentration
ax = axes[0]
for label, marker, color in [(0, 'o', 'blue'), (1, '^', 'red')]:
    subset = df[df['is_anomaly']==label]
    ax.scatter(subset['seasonal_entropy'], subset['seasonal_max_share'], 
               alpha=0.5, s=50, marker=marker, color=color, 
               label=f"{'Anomaly' if label else 'Non-Anomaly'}")
ax.set_xlabel('Seasonal Entropy (1=balanced)', fontsize=11)
ax.set_ylabel('Max Quarterly Share', fontsize=11)
ax.set_title('Seasonal Balance: Anomaly vs Non-Anomaly', fontsize=12)
ax.legend()
ax.grid(alpha=0.3)

# Stacked bar - avg quarterly distribution by segment
ax = axes[1]
seg_order = ['Basic', 'Growing', 'Standard', 'High Value', 'Premium']
q_data = df.groupby('profitability_segment')[['q1_transactions','q2_transactions','q3_transactions','q4_transactions']].mean()
q_data = q_data.div(q_data.sum(axis=1), axis=0)
q_data.loc[seg_order].T.plot(kind='bar', stacked=True, ax=ax, alpha=0.8)
ax.set_title('Quarterly Transaction Distribution by Segment', fontsize=12)
ax.set_ylabel('Share of Transactions')
ax.set_xlabel('Quarter')
ax.legend(title='Segment', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('/work/seasonal_analysis.png', dpi=150)
plt.close()

# FIGURE 3: Value alignment scatter
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['blue' if a == 0 else 'red' for a in df['is_anomaly']]
sizes = [30 if a == 0 else 50 for a in df['is_anomaly']]
sc = ax.scatter(df['total_revenue'], df['comprehensive_customer_score'], 
                c=colors, s=sizes, alpha=0.6, edgecolors='k', linewidth=0.5)
# Regression line
from scipy import stats
slope, intercept, r, p, se = stats.linregress(df['total_revenue'], df['comprehensive_customer_score'])
x_line = np.linspace(df['total_revenue'].min(), df['total_revenue'].max(), 100)
ax.plot(x_line, intercept + slope*x_line, 'k--', alpha=0.5, label=f'Regression (r={r:.3f})')
ax.set_xlabel('Total Revenue', fontsize=12)
ax.set_ylabel('Comprehensive Customer Score', fontsize=12)
ax.set_title('Value Realization: Score vs Revenue by Anomaly Status', fontsize=13)
# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='blue', label='Non-Anomaly'),
                   Patch(facecolor='red', label='Anomaly'),
                   plt.Line2D([0], [0], color='k', linestyle='--', label=f'Regression (r={r:.3f})')]
ax.legend(handles=legend_elements, loc='lower right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/value_alignment.png', dpi=150)
plt.close()

# FIGURE 4: Transaction consistency comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
for label, color, marker in [(0, 'blue', 'o'), (1, 'red', '^')]:
    subset = df[df['is_anomaly']==label]
    ax.scatter(subset['transaction_count'], subset['avg_transactions_per_month'], 
               alpha=0.5, s=50, color=color, marker=marker, 
               label=f"{'Anomaly' if label else 'Non-Anomaly'}")
ax.set_xlabel('Transaction Count', fontsize=11)
ax.set_ylabel('Avg Transactions per Month', fontsize=11)
ax.set_title('Transactions: Count vs Monthly Rate', fontsize=12)
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
for label, color, marker in [(0, 'blue', 'o'), (1, 'red', '^')]:
    subset = df[df['is_anomaly']==label]
    ax.scatter(subset['transaction_value_volatility'], subset['tx_ratio'], 
               alpha=0.5, s=50, color=color, marker=marker,
               label=f"{'Anomaly' if label else 'Non-Anomaly'}")
ax.set_xlabel('Transaction Value Volatility', fontsize=11)
ax.set_ylabel('Transaction Consistency Ratio', fontsize=11)
ax.set_title('Volatility vs Consistency Ratio', fontsize=12)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/transactional_analysis.png', dpi=150)
plt.close()

# FIGURE 5: Cluster profiles
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
cluster_cols = ['transaction_value_volatility', 'tx_ratio', 'seasonal_std', 
                'score_rev_resid', 'comprehensive_customer_score', 'total_revenue']
titles = ['Transaction Volatility', 'Tx Consistency Ratio', 'Seasonal Concentration',
          'Score-Revenue Residual', 'Customer Score', 'Total Revenue']
for ax, col, title in zip(axes.flatten(), cluster_cols, titles):
    for clust in range(4):
        subset = df[df['cluster']==clust]
        ax.hist(subset[col], bins=10, alpha=0.5, label=f'C{clust}', density=True)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('')
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('/work/cluster_profiles.png', dpi=150)
plt.close()

# FIGURE 6: Anomaly rate by cluster
fig, ax = plt.subplots(figsize=(8, 5))
cluster_rates = df.groupby('cluster')['is_anomaly'].mean() * 100
cluster_counts = df.groupby('cluster').size()
ax.bar(range(4), cluster_rates, color=['steelblue', 'orange', 'green', 'crimson'], alpha=0.7)
for i, (rate, cnt) in enumerate(zip(cluster_rates, cluster_counts)):
    ax.text(i, rate+1, f'n={cnt}\n{rate:.1f}%', ha='center', fontsize=11)
ax.set_xticks(range(4))
ax.set_xticklabels([f'Cluster {i}' for i in range(4)])
ax.set_ylabel('% Anomaly', fontsize=12)
ax.set_title('Anomaly Rate by Cluster', fontsize=13)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/cluster_anomaly_rate.png', dpi=150)
plt.close()

# FIGURE 7: Decision tree schematic (text-based) - visual summary
fig, ax = plt.subplots(figsize=(14, 8))
ax.axis('off')
ax.set_title('Decision Tree Key Splits for Anomaly Prediction', fontsize=14, fontweight='bold')
# Create a visual tree
tree_text = """
                           [Total Revenue]
                           /             \\
                    ≤ 799.5             > 799.5
                    /                         \\
           [Total Revenue]              [Tx Consistency Ratio]
            /           \\                  /               \\
         ≤ 592.6      > 592.6           ≤ 0.454          > 0.454
          /               \\              /                    \\
   [Total Revenue]    0% anomaly    100% anomaly        [Score Residual]
    /           \\         (n=52)         (n=12)           /           \\
 ≤ 405.2      > 405.2                                  ≤ 3.12       > 3.12
   /              \\                                       /              \\
[Revenue ≤ 196.6]  [Volatility]                        25% anomaly     85.7% anomaly
  /         \\        /         \\                         (n=8)          (n=7)
83.3%    0%       16.7%     87.5%
anomaly  anomaly  anomaly   anomaly
(n=18)   (n=30)   (n=6)     (n=16)
"""
ax.text(0.5, 0.5, tree_text, transform=ax.transAxes, fontsize=9, fontfamily='monospace',
        verticalalignment='center', horizontalalignment='center')
plt.tight_layout()
plt.savefig('/work/decision_tree_schematic.png', dpi=150)
plt.close()

print("All figures saved.")
print("Files in /work:", [f for f in __import__('os').listdir('/work') if f.endswith('.png')])