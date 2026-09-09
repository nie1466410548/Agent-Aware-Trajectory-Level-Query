import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ========== FIGURE 1: Feature AUC Comparison ==========
features = ['Negative Sentiment Trend', 'Health Score', 'Education Focus', 'Last Value Milestone', 
            'Average Resolution Time', 'Time Since Milestone', 'Feature Adoption Coverage',
            'Reopen Proportion', 'Conversation Rate (30d)']
aucs = [1.0, 1.0, 0.95, 0.92, 0.50, 0.50, 0.46, 0.48, 0.49]
colors = ['#27ae60' if a >= 0.7 else '#f39c12' if a >= 0.6 else '#e74c3c' for a in aucs]

plt.figure(figsize=(12, 6))
bars = plt.barh(range(len(features)), aucs, color=colors, edgecolor='gray', linewidth=0.5)
plt.yticks(range(len(features)), features)
plt.xlabel('AUC (Discriminative Power)', fontsize=12)
plt.title('Renewal Risk Feature Discriminative Power\n(Historical Cohort: Renewed vs Churned)', fontsize=14, fontweight='bold')
plt.axvline(0.5, color='gray', linestyle='--', alpha=0.5, label='Random (AUC=0.5)')
plt.axvline(0.7, color='green', linestyle='--', alpha=0.4, label='Strong (AUC=0.7)')
plt.axvline(0.6, color='orange', linestyle='--', alpha=0.4, label='Moderate (AUC=0.6)')
plt.xlim(0, 1.05)
plt.legend()
plt.tight_layout()
plt.savefig('feature_auc_comparison.png', dpi=100)
print("Saved: feature_auc_comparison.png")

# ========== FIGURE 2: Industry Risk Heatmap ==========
industries = ['SaaS', 'Financial Services', 'Hospitality', 'Healthcare', 'Retail & eCommerce', 
              'Professional Services', 'Education Technology', 'Energy & Utilities', 'Manufacturing',
              'Telecommunications', 'Gaming & Media', 'Logistics']
at_risk_rate = [0.50, 0.49, 0.45, 0.44, 0.42, 0.41, 0.41, 0.37, 0.37, 0.36, 0.31, 0.27]
n_companies = [38, 37, 33, 32, 33, 32, 37, 38, 38, 36, 32, 33]

plt.figure(figsize=(10, 7))
# Sort by risk rate
sorted_idx = np.argsort(at_risk_rate)
industries_sorted = [industries[i] for i in sorted_idx]
rates_sorted = [at_risk_rate[i] for i in sorted_idx]
n_sorted = [n_companies[i] for i in sorted_idx]

colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(industries_sorted)))
bars = plt.barh(range(len(industries_sorted)), rates_sorted, color=colors, edgecolor='gray')
plt.yticks(range(len(industries_sorted)), industries_sorted)
plt.xlabel('At-Risk Rate', fontsize=12)
plt.title('Renewal Risk by Industry\n(Target Population: Renewal within 90 days)', fontsize=14, fontweight='bold')
for i, (rate, n) in enumerate(zip(rates_sorted, n_sorted)):
    plt.text(rate + 0.01, i, f'{rate:.0%} (n={n})', va='center', fontsize=10)
plt.xlim(0, 0.7)
plt.tight_layout()
plt.savefig('industry_risk.png', dpi=100)
print("Saved: industry_risk.png")

# ========== FIGURE 3: Contract Size Risk ==========
sizes = ['small', 'mid', 'large', 'strategic']
size_risk = [0.44, 0.44, 0.38, 0.37]
size_n = [89, 101, 125, 104]

plt.figure(figsize=(8, 5))
colors_size = ['#e74c3c' if r >= 0.4 else '#f39c12' if r >= 0.35 else '#27ae60' for r in size_risk]
bars = plt.bar(sizes, size_risk, color=colors_size, edgecolor='gray', width=0.5)
plt.xlabel('Contract Size', fontsize=12)
plt.ylabel('At-Risk Rate', fontsize=12)
plt.title('Renewal Risk by Contract Size', fontsize=14, fontweight='bold')
for bar, rate, n in zip(bars, size_risk, size_n):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{rate:.0%} (n={n})', ha='center', fontsize=11)
plt.ylim(0, 0.6)
plt.tight_layout()
plt.savefig('contract_size_risk.png', dpi=100)
print("Saved: contract_size_risk.png")

# ========== FIGURE 4: Feature comparison (key features) ==========
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Data for the 2 key features with strong separation
# 1. Sentiment trend
trend_labels = ['at-risk', 'watch', 'stable', 'uplift', 'positive']
renewed_counts = [0, 0, 167, 251, 501]
churned_counts = [502, 502, 0, 0, 0]

ax1 = axes[0, 0]
x = np.arange(len(trend_labels))
width = 0.35
ax1.bar(x - width/2, renewed_counts, width, label='Renewed', color='#27ae60')
ax1.bar(x + width/2, churned_counts, width, label='Churned', color='#e74c3c')
ax1.set_xticks(x)
ax1.set_xticklabels(trend_labels, rotation=45, ha='right')
ax1.set_title('Sentiment Trend\n(Perfect Separator)', fontsize=12)
ax1.legend(fontsize=9)

# 2. Health score
ax2 = axes[0, 1]
health_bins = ['52-59', '60-69', '70-79', '80-87']
renewed_h = [0, 0, 0, 919]
churned_h = [675, 329, 0, 0]
ax2.bar(x[:4] - width/2, renewed_h, width, label='Renewed', color='#27ae60')
ax2.bar(x[:4] + width/2, churned_h, width, label='Churned', color='#e74c3c')
ax2.set_xticks(x[:4])
ax2.set_xticklabels(health_bins)
ax2.set_title('Health Score Distribution\n(Perfect Separator)', fontsize=12)
ax2.legend(fontsize=9)

# 3. Education focus
ax3 = axes[0, 2]
edu_labels = ['AI Enablement', 'Adoption', 'Analytics', 'Integration', 'Onboarding', 'Security', 'Workflow Auto']
renewed_e = [250, 84, 167, 84, 84, 0, 0]
churned_e = [0, 0, 0, 0, 0, 251, 251]
x_edu = np.arange(len(edu_labels))
ax3.bar(x_edu - width/2, renewed_e, width, label='Renewed', color='#27ae60')
ax3.bar(x_edu + width/2, churned_e, width, label='Churned', color='#e74c3c')
ax3.set_xticks(x_edu)
ax3.set_xticklabels(edu_labels, rotation=45, ha='right')
ax3.set_title('Education Focus', fontsize=12)
ax3.legend(fontsize=9)

# 4. Feature adoption comparison
ax4 = axes[1, 0]
# Full population data
adopt_bins = ['55-64', '65-74', '75-84', '85-94']
renewed_a = [250, 250, 251, 168]
churned_a = [250, 251, 251, 252]
x_a = np.arange(len(adopt_bins))
ax4.bar(x_a - width/2, renewed_a, width, label='Renewed', color='#27ae60')
ax4.bar(x_a + width/2, churned_a, width, label='Churned', color='#e74c3c')
ax4.set_xticks(x_a)
ax4.set_xticklabels(adopt_bins)
ax4.set_title('Feature Adoption Coverage\n(Weak Discriminator)', fontsize=12)
ax4.legend(fontsize=9)

# 5. ACV comparison
ax5 = axes[1, 1]
acv_bins = ['<$20k', '$20-50k', '$50-100k', '$100k+']
renewed_acv = [200, 300, 200, 219]
churned_acv = [250, 350, 250, 154]
x_acv = np.arange(len(acv_bins))
ax5.bar(x_acv - width/2, renewed_acv, width, label='Renewed', color='#27ae60')
ax5.bar(x_acv + width/2, churned_acv, width, label='Churned', color='#e74c3c')
ax5.set_xticks(x_acv)
ax5.set_xticklabels(acv_bins)
ax5.set_title('ACV Distribution', fontsize=12)
ax5.legend(fontsize=9)

# 6. Last value milestone
ax6 = axes[1, 2]
mstone_labels = ['Usage Insights', 'ROI Review', 'Dashboard', 'Mobile Rollout', 'Security Audit', 'Billing Integration']
renewed_m = [251, 251, 251, 167, 0, 0]
churned_m = [0, 0, 0, 0, 250, 251]
x_m = np.arange(len(mstone_labels))
ax6.bar(x_m - width/2, renewed_m, width, label='Renewed', color='#27ae60')
ax6.bar(x_m + width/2, churned_m, width, label='Churned', color='#e74c3c')
ax6.set_xticks(x_m)
ax6.set_xticklabels(mstone_labels, rotation=45, ha='right')
ax6.set_title('Last Value Milestone Type', fontsize=12)
ax6.legend(fontsize=9)

plt.suptitle('Renewal Risk Feature Analysis: Renewed vs Churned\n(Full Population with Expansion Signal as Outcome Proxy)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('feature_comparison_grid.png', dpi=100, bbox_inches='tight')
print("Saved: feature_comparison_grid.png")