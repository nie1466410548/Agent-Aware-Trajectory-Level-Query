import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load saved data
df = pd.read_pickle('/work/analysis_data.pkl')

# Set style
plt.rcParams.update({'figure.max_open_warning': 0, 'font.size': 11})
sns.set_style("whitegrid")
palette = {'HVE': '#E74C3C', 'SMB': '#3498DB'}

# ========== FIGURE 1: RFM Component Comparison ==========
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
rfm_cols = ['recency_score', 'frequency_score', 'monetary_score']
titles = ['Recency Score', 'Frequency Score', 'Monetary Score']
for i, (col, title) in enumerate(zip(rfm_cols, titles)):
    for grp in ['HVE', 'SMB']:
        data = df[df['customer_group']==grp][col]
        axes[i].hist(data, bins=range(1,7), alpha=0.6, label=grp, 
                     color=palette[grp], density=True, align='left')
    axes[i].set_title(title, fontsize=13, fontweight='bold')
    axes[i].set_xlabel('Score')
    axes[i].set_ylabel('Density')
    axes[i].legend()
    axes[i].set_xticks([1,2,3,4,5])
plt.tight_layout()
plt.savefig('/work/fig1_rfm_components.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig1 saved")

# ========== FIGURE 2: M-RF Gap Distribution ==========
fig, ax = plt.subplots(figsize=(10, 5))
for grp in ['HVE', 'SMB']:
    data = df[df['customer_group']==grp]['m_rf_gap']
    ax.hist(data, bins=30, alpha=0.6, label=f'{grp} (n={len(data)})', 
            color=palette[grp], density=True)
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5, label='Balance (gap=0)')
ax.set_xlabel('Monetary - (Recency+Frequency)/2 (M-RF Gap)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Value-Engagement Gap: M-RF Gap Distribution\n(Positive = Monetary exceeds Engagement)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('/work/fig2_mrf_gap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig2 saved")

# ========== FIGURE 3: LTV vs RFM Consistency Scatter ==========
fig, ax = plt.subplots(figsize=(10, 6))
for grp in ['HVE', 'SMB']:
    sub = df[df['customer_group']==grp]
    # Use log scale for LTV
    ax.scatter(sub['rfm_std'], sub['estimated_customer_ltv'], 
               c=palette[grp], label=grp, alpha=0.5, s=30, edgecolors='none')
ax.set_xlabel('RFM Consistency (std of R,F,M) — Higher = Less Consistent', fontsize=12)
ax.set_ylabel('Estimated Customer LTV ($)', fontsize=12)
ax.set_title('LTV vs RFM Consistency: The Paradox\n(HVE: High Value, Low Consistency)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.set_yscale('symlog')
plt.tight_layout()
plt.savefig('/work/fig3_ltv_vs_consistency.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig3 saved")

# ========== FIGURE 4: Lifecycle Stage by Group ==========
fig, ax = plt.subplots(figsize=(10, 5))
lifecycle_order = ['Activation', 'Growth', 'Maturity', 'Retention', 'Dormant']
lifecycle_data = pd.crosstab(df['customer_group'], df['lifecycle_stage'], normalize='index')[lifecycle_order]
lifecycle_data.plot(kind='bar', ax=ax, color=['#2ECC71','#F39C12','#9B59B6','#E74C3C','#95A5A6'])
ax.set_title('Lifecycle Stage Distribution by Customer Group', fontsize=14, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Proportion', fontsize=12)
ax.legend(title='Lifecycle Stage', fontsize=9)
ax.set_xticklabels(['HVE (n=91)', 'SMB (n=4581)'], rotation=0)
plt.tight_layout()
plt.savefig('/work/fig4_lifecycle.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig4 saved")

# ========== FIGURE 5: Risk Category Comparison ==========
fig, ax = plt.subplots(figsize=(10, 5))
risk_order = ['Minimal Risk', 'Low Risk', 'Medium Risk', 'High Risk']
risk_data = pd.crosstab(df['customer_group'], df['risk_category'], normalize='index')[risk_order]
risk_data.plot(kind='bar', ax=ax, color=['#2ECC71','#27AE60','#F39C12','#E74C3C'])
ax.set_title('Risk Category Distribution by Customer Group', fontsize=14, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Proportion', fontsize=12)
ax.legend(title='Risk Category', fontsize=9)
ax.set_xticklabels(['HVE (n=91)', 'SMB (n=4581)'], rotation=0)
plt.tight_layout()
plt.savefig('/work/fig5_risk.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig5 saved")

# ========== FIGURE 6: Value Stability ==========
fig, ax = plt.subplots(figsize=(10, 5))
stab_order = ['Unstable', 'Low Stability', 'Medium Stability']
stab_data = pd.crosstab(df['customer_group'], df['value_stability'], normalize='index')[stab_order]
stab_data.plot(kind='bar', ax=ax, color=['#E74C3C','#F39C12','#2ECC71'])
ax.set_title('Value Stability Distribution by Customer Group', fontsize=14, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Proportion', fontsize=12)
ax.legend(title='Value Stability', fontsize=9)
ax.set_xticklabels(['HVE (n=91)', 'SMB (n=4581)'], rotation=0)
plt.tight_layout()
plt.savefig('/work/fig6_stability.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig6 saved")

# ========== FIGURE 7: Strategic Classification ==========
fig, ax = plt.subplots(figsize=(10, 5))
strat_order = ['Standard Account', 'Recovery Account', 'Key Account', 'Strategic Account']
strat_data = pd.crosstab(df['customer_group'], df['strategic_classification'], normalize='index')[strat_order]
strat_data.plot(kind='bar', ax=ax, color=['#95A5A6','#F39C12','#9B59B6','#E74C3C'])
ax.set_title('Strategic Classification by Customer Group', fontsize=14, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Proportion', fontsize=12)
ax.legend(title='Classification', fontsize=9)
ax.set_xticklabels(['HVE (n=91)', 'SMB (n=4581)'], rotation=0)
plt.tight_layout()
plt.savefig('/work/fig7_strategic.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig7 saved")

# ========== FIGURE 8: Composite RFM Score Comparison ==========
fig, ax = plt.subplots(figsize=(10, 5))
for grp in ['HVE', 'SMB']:
    data = df[df['customer_group']==grp]['composite_rfm']
    ax.hist(data, bins=20, alpha=0.6, label=f'{grp} (n={len(data)})', 
            color=palette[grp], density=True)
ax.set_xlabel('Composite RFM Score (0.35R+0.3F+0.35M)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Composite RFM Score Distribution', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('/work/fig8_composite_rfm.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig8 saved")

# ========== FIGURE 9: Upsell / Development ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# Upsell potential
upsell_data = pd.crosstab(df['customer_group'], df['upsell_potential'], normalize='index')
upsell_data.plot(kind='bar', ax=axes[0], color=['#2ECC71','#E74C3C'])
axes[0].set_title('Upsell Potential', fontsize=13, fontweight='bold')
axes[0].set_xlabel('')
axes[0].set_ylabel('Proportion')
axes[0].set_xticklabels(['HVE', 'SMB'], rotation=0)
# Development opportunity
dev_data = pd.crosstab(df['customer_group'], df['development_opportunity'], normalize='index')
dev_data.plot(kind='bar', ax=axes[1], color=['#3498DB','#E74C3C'])
axes[1].set_title('Development Opportunity', fontsize=13, fontweight='bold')
axes[1].set_xlabel('')
axes[1].set_ylabel('Proportion')
axes[1].set_xticklabels(['HVE', 'SMB'], rotation=0)
plt.tight_layout()
plt.savefig('/work/fig9_upsell_dev.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig9 saved")

print("\nAll figures saved successfully!")