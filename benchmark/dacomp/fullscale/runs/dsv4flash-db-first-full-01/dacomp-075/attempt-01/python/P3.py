import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/focus_group_with_scores.csv')

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
sns.set_style("whitegrid")

# ==========================================
# FIGURE 1: Heatmap of top 15 vendors by spend
# ==========================================
top15 = df.nlargest(15, 'total_vendor_spend').copy()
top15 = top15.sort_values('overall_resilience', ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Left: Heatmap of 4 dimensions
heatmap_data = top15[['financial_resilience', 'operational_resilience', 
                       'market_resilience', 'strategic_resilience']]
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn', 
            xticklabels=['Financial', 'Operational', 'Market', 'Strategic'],
            yticklabels=top15['vendor_name'].values, ax=axes[0], 
            vmin=0, vmax=100, cbar_kws={'label': 'Resilience Score (0-100)'})
axes[0].set_title('Multi-Dimensional Resilience Scores\n(Top 15 Vendors by Spend)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Resilience Dimension')
axes[0].set_ylabel('Vendor')

# Right: Overall resilience with error bars (range of dimensions)
dim_scores = top15[['financial_resilience', 'operational_resilience', 
                     'market_resilience', 'strategic_resilience']].values
means = dim_scores.mean(axis=1)
mins = dim_scores.min(axis=1)
maxs = dim_scores.max(axis=1)

y_pos = np.arange(len(top15))
axes[1].barh(y_pos, top15['overall_resilience'].values, color='steelblue', alpha=0.8)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(top15['vendor_name'].values)
axes[1].axvline(x=50, color='red', linestyle='--', alpha=0.5, label='Medium Threshold')
axes[1].axvline(x=70, color='green', linestyle='--', alpha=0.5, label='High Threshold')
axes[1].set_xlabel('Overall Resilience Score')
axes[1].set_title('Overall Resilience Score\n(Top 15 Vendors by Spend)', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].set_xlim(0, 100)

plt.tight_layout()
plt.savefig('/work/figure1_resilience_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 1 saved")

# ==========================================
# FIGURE 2: Radar chart for top 5 strategic vendors
# ==========================================
top5_strategic = df.nlargest(5, 'total_vendor_spend').copy()

categories = ['Financial\nResilience', 'Operational\nResilience', 
              'Market\nResilience', 'Strategic\nResilience']
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
for i, (_, row) in enumerate(top5_strategic.iterrows()):
    values = [row['financial_resilience'], row['operational_resilience'], 
              row['market_resilience'], row['strategic_resilience']]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=row['vendor_name'], color=colors[i])
    ax.fill(angles, values, alpha=0.1, color=colors[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
ax.set_title('Vendor Resilience Radar - Top 5 Strategic Vendors', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('/work/figure2_resilience_radar.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 2 saved")

# ==========================================
# FIGURE 3: Distribution of scores
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

dimensions = [
    ('financial_resilience', 'Financial Resilience'),
    ('operational_resilience', 'Operational Resilience'),
    ('market_resilience', 'Market Resilience'),
    ('strategic_resilience', 'Strategic Resilience')
]

for ax, (col, title) in zip(axes.flatten(), dimensions):
    scores = df[col].values
    ax.hist(scores, bins=15, color='steelblue', edgecolor='white', alpha=0.7)
    ax.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, 
               label=f'Mean={np.mean(scores):.1f}')
    ax.axvline(np.median(scores), color='green', linestyle='-.', linewidth=2, 
               label=f'Median={np.median(scores):.1f}')
    ax.set_xlabel('Score')
    ax.set_ylabel('Number of Vendors')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)

plt.suptitle('Distribution of Resilience Scores Across Dimensions\n(N=91 Key Vendors)', 
             fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('/work/figure3_score_distributions.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 3 saved")

# ==========================================
# FIGURE 4: Category-level resilience comparison
# ==========================================
fig, ax = plt.subplots(figsize=(14, 6))

cat_data = df.groupby('vendor_category_name')[['financial_resilience', 'operational_resilience', 
                                                'market_resilience', 'strategic_resilience']].mean()

x = np.arange(len(cat_data))
width = 0.2

ax.bar(x - 1.5*width, cat_data['financial_resilience'], width, label='Financial', color='#e74c3c')
ax.bar(x - 0.5*width, cat_data['operational_resilience'], width, label='Operational', color='#3498db')
ax.bar(x + 0.5*width, cat_data['market_resilience'], width, label='Market', color='#2ecc71')
ax.bar(x + 1.5*width, cat_data['strategic_resilience'], width, label='Strategic', color='#f39c12')

ax.set_xticks(x)
ax.set_xticklabels(cat_data.index, rotation=30, ha='right')
ax.set_ylabel('Average Resilience Score')
ax.set_title('Resilience Scores by Vendor Category', fontsize=14, fontweight='bold')
ax.legend()
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('/work/figure4_category_resilience.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 4 saved")

# ==========================================
# FIGURE 5: Spend vs Resilience scatter
# ==========================================
fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(df['total_vendor_spend'], df['overall_resilience'], 
                     c=df['vendor_risk_score'], cmap='RdYlGn_r', s=80, alpha=0.7, 
                     edgecolors='black', linewidth=0.5)

# Label top vendors
for _, row in df.nlargest(10, 'total_vendor_spend').iterrows():
    ax.annotate(row['vendor_name'][:20], 
                (row['total_vendor_spend'], row['overall_resilience']),
                fontsize=8, alpha=0.8, ha='center', va='bottom')

ax.set_xlabel('Total Vendor Spend ($)', fontsize=12)
ax.set_ylabel('Overall Resilience Score', fontsize=12)
ax.set_title('Vendor Spend vs. Overall Resilience\n(Colored by Risk Score)', fontsize=14, fontweight='bold')
cbar = plt.colorbar(scatter)
cbar.set_label('Vendor Risk Score (lower = better)')

# Add threshold lines
ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Resilience Threshold')
ax.axvline(x=500000, color='orange', linestyle=':', alpha=0.5, label='High Spend Threshold')
ax.legend()

ax.set_xscale('symlog')
plt.tight_layout()
plt.savefig('/work/figure5_spend_vs_resilience.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 5 saved")

# Print summary statistics
print("\n=== DIMENSION CORRELATIONS ===")
corr = df[['financial_resilience', 'operational_resilience', 'market_resilience', 
           'strategic_resilience', 'overall_resilience', 'total_vendor_spend']].corr()
print(corr.round(3))