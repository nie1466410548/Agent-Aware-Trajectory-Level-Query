import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('/work/risk_warning_results.csv')
best_df = pd.read_csv('/work/refined_best_strategy.csv')

# Reconstruct key high-risk vendors (spend > $1M and disruption prob >= 60)
high_risk = df[df['disruption_probability_12_18mo'] >= 60].copy()
key_high_risk = high_risk[high_risk['total_vendor_spend'] > 1000000].sort_values(
    'disruption_probability_12_18mo', ascending=False)

# Contingency plan logic
def contingency_plan(prob, dependency, activity):
    if prob >= 75:
        return ('IMMEDIATE ACTION: Freeze new orders, activate approved alternative suppliers, '
                'initiate urgent contract renegotiation, escalate to executive risk committee, '
                'establish daily monitoring cadence and 30-day emergency inventory buffer.')
    elif prob >= 65:
        return ('SHORT-TERM ACTION (30-60 days): Qualify and contract backup suppliers, '
                'reduce single-source dependency, renegotiate payment terms, '
                'implement weekly risk monitoring and quarterly business continuity reviews.')
    else:
        return ('ELEVATED MONITORING: Formalize alternative supplier shortlist, '
                'conduct quarterly financial health reviews, align contract renewals, '
                'maintain communication channels and define trigger thresholds for escalation.')

key_high_risk = key_high_risk.copy()
key_high_risk['contingency_plan'] = key_high_risk.apply(
    lambda r: contingency_plan(r['disruption_probability_12_18mo'], r['dependency_level'], r['activity_status']), axis=1)

# Merge optimal strategy
key_high_risk = key_high_risk.merge(best_df[['vendor_id', 'best_strategy', 'best_roi']], on='vendor_id', how='left')

# Build final summary table for report
summary = key_high_risk[['vendor_name', 'vendor_category_name', 'total_vendor_spend', 
                          'disruption_probability_12_18mo', 'warning_level', 
                          'financial_resilience', 'operational_resilience', 'market_resilience', 'strategic_resilience',
                          'overall_resilience', 'dependency_level', 'activity_status', 
                          'contract_expiry_date', 'best_strategy', 'best_roi']].copy()
summary = summary.sort_values('disruption_probability_12_18mo', ascending=False)

print("=== FINAL KEY HIGH-RISK VENDOR SUMMARY ===")
for _, r in summary.iterrows():
    print(f"{r['vendor_name'][:28]:30s} | ${r['total_vendor_spend']:>9,.0f} | Prob={r['disruption_probability_12_18mo']:.0f} | "
          f"{r['best_strategy'][:28]:28s} | ROI={r['best_roi']:.0f}%")

summary.to_csv('/work/final_key_vendor_summary.csv', index=False)

# FIGURE 10: Key vendor risk-return quadrant
fig, ax = plt.subplots(figsize=(12, 8))
# All vendors as background
ax.scatter(df['overall_resilience'], df['disruption_probability_12_18mo'], 
           alpha=0.3, s=30, color='gray', label='All Key Vendors (91)')
# Key high-risk highlighted
ax.scatter(key_high_risk['overall_resilience'], key_high_risk['disruption_probability_12_18mo'], 
           s=key_high_risk['total_vendor_spend']/30000, alpha=0.8, edgecolors='black', linewidth=0.5,
           color='#e74c3c', label='Key High-Risk (>$1M spend)')

# Annotate
for _, r in key_high_risk.iterrows():
    ax.annotate(r['vendor_name'][:18], (r['overall_resilience'], r['disruption_probability_12_18mo']),
                fontsize=7.5, ha='center', va='bottom', alpha=0.9)

ax.axhline(60, color='red', linestyle='--', alpha=0.6, label='High Risk Threshold')
ax.axvline(50, color='blue', linestyle='--', alpha=0.6, label='Medium Resilience Threshold')
ax.set_xlabel('Overall Resilience Score')
ax.set_ylabel('12-18 Month Disruption Probability')
ax.set_title('Key Vendor Risk Quadrant: Resilience vs. Disruption Risk', fontsize=15, fontweight='bold')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/work/figure10_risk_quadrant.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigure 10 saved")

# FIGURE 11: Warning mechanism - indicator breakdown for top 5 key vendors
top5 = key_high_risk.head(5)
ind_cols = ['fin_distress_risk', 'dependency_risk', 'activity_risk', 'contract_expiry_risk', 
            'operational_weakness_risk', 'market_risk', 'concentration_risk']
ind_labels = ['Financial', 'Dependency', 'Activity', 'Contract\nExpiry', 'Operational', 'Market', 'Concentration']

fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(ind_labels))
width = 0.15
colors = ['#c0392b', '#e67e22', '#f1c40f', '#27ae60', '#3498db', '#9b59b6', '#34495e']
for i, (_, r) in enumerate(top5.iterrows()):
    vals = [r[c] for c in ind_cols]
    ax.bar(x + i*width, vals, width, label=r['vendor_name'][:20], color=colors[i], alpha=0.85)

ax.set_xticks(x + width*2)
ax.set_xticklabels(ind_labels, fontsize=10)
ax.set_ylabel('Risk Indicator Score (0-100)')
ax.set_title('Risk Indicator Breakdown - Top 5 Key High-Risk Vendors', fontsize=14, fontweight='bold')
ax.legend(fontsize=8, ncol=2)
ax.set_ylim(0, 110)
plt.tight_layout()
plt.savefig('/work/figure11_risk_indicator_breakdown.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 11 saved")

# FIGURE 12: Sensitivity analysis of ROI (S2 diversification)
# ROI vs probability reduction for key strategy
fig, ax = plt.subplots(figsize=(10, 6))
prob_reductions = np.arange(0.05, 0.6, 0.05)
# Compute portfolio-wide ROI for S2 with varying prob reduction
annual_loss = df['expected_annual_loss'].sum()
annual_cost_s2 = df['total_vendor_spend'].sum() * 0.025
roi_curve = [(annual_loss * pr * 3 - annual_cost_s2 * 3) / (annual_cost_s2 * 3) * 100 for pr in prob_reductions]
ax.plot(prob_reductions*100, roi_curve, 'o-', color='#e67e22', linewidth=2, markersize=6)
ax.axhline(0, color='black', linestyle='--')
ax.axvline(35, color='red', linestyle='--', alpha=0.5, label='Assumed 35% reduction')
ax.set_xlabel('Probability Reduction Achieved (%)')
ax.set_ylabel('Portfolio ROI (%) - 3yr')
ax.set_title('ROI Sensitivity: Supplier Diversification (S2)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/figure12_roi_sensitivity.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 12 saved")