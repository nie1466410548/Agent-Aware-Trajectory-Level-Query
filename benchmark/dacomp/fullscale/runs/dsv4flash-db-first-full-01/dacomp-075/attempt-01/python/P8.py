import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('/work/risk_warning_results.csv')

# Recompute refined expected loss (same model as P6)
impact_mult = {'Critical Impact': 2.0, 'High Impact': 1.5, 'Moderate Impact': 1.2, 'Low Impact': 1.0}
df['impact_multiplier'] = df['business_impact_level'].map(impact_mult).fillna(1.2)
df['expected_annual_loss'] = (df['total_vendor_spend'] * 
                              (df['disruption_probability_12_18mo'] / 100) * 
                              df['impact_multiplier'] * 0.15)

# Sensitivity: S2 supplier diversification and S1 financial
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
prob_reductions = np.arange(0.05, 0.6, 0.05)
annual_loss = df['expected_annual_loss'].sum()
total_spend = df['total_vendor_spend'].sum()

# S2: cost rate 2.5%
annual_cost_s2 = total_spend * 0.025
roi_s2 = [(annual_loss * pr * 3 - annual_cost_s2 * 3) / (annual_cost_s2 * 3) * 100 for pr in prob_reductions]
axes[0].plot(prob_reductions*100, roi_s2, 'o-', color='#e67e22', linewidth=2, markersize=6)
axes[0].axhline(0, color='black', linestyle='--')
axes[0].axvline(35, color='red', linestyle='--', alpha=0.5, label='Assumed 35% reduction')
axes[0].set_xlabel('Probability Reduction Achieved (%)')
axes[0].set_ylabel('Portfolio ROI (%) - 3yr')
axes[0].set_title('ROI Sensitivity: Supplier Diversification (S2)', fontsize=13, fontweight='bold')
axes[0].legend()

# S1: cost rate 0.5%
annual_cost_s1 = total_spend * 0.005
roi_s1 = [(annual_loss * pr * 3 - annual_cost_s1 * 3) / (annual_cost_s1 * 3) * 100 for pr in prob_reductions]
axes[1].plot(prob_reductions*100, roi_s1, 's-', color='#27ae60', linewidth=2, markersize=6)
axes[1].axhline(0, color='black', linestyle='--')
axes[1].axvline(25, color='red', linestyle='--', alpha=0.5, label='Assumed 25% reduction')
axes[1].set_xlabel('Probability Reduction Achieved (%)')
axes[1].set_ylabel('Portfolio ROI (%) - 3yr')
axes[1].set_title('ROI Sensitivity: Financial Restructuring (S1)', fontsize=13, fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/figure12_roi_sensitivity.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 12 saved")

# Also create a summary figure: strategy cost vs benefit bubble
fig, ax = plt.subplots(figsize=(10, 7))
# Load refined ROI
roi = pd.read_csv('/work/refined_roi.csv')
scatter = ax.scatter(roi['annual_cost'], roi['annual_benefit'], s=roi['net_benefit_3yr']/500, 
                     c=roi['roi_pct'], cmap='RdYlGn', alpha=0.85, edgecolors='black', linewidth=0.5)
for _, r in roi.iterrows():
    ax.annotate(r['strategy'].split(': ')[1][:22], (r['annual_cost'], r['annual_benefit']), fontsize=8)
ax.set_xlabel('Annual Strategy Cost ($)')
ax.set_ylabel('Annual Risk Reduction Benefit ($)')
ax.set_title('Resilience Strategy Trade-off: Cost vs. Benefit', fontsize=14, fontweight='bold')
ax.plot([0, max(roi['annual_cost'].max(), roi['annual_benefit'].max())], 
        [0, max(roi['annual_cost'].max(), roi['annual_benefit'].max())], 'k--', alpha=0.3, label='Breakeven line')
cbar = plt.colorbar(scatter)
cbar.set_label('ROI (%)')
ax.legend()
plt.tight_layout()
plt.savefig('/work/figure13_strategy_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 13 saved")

# Summary stats for report
print("\n=== REPORT METRICS ===")
print(f"Vendors in focus group: {len(df)}")
print(f"High-risk (prob>=60): {(df['disruption_probability_12_18mo']>=60).sum()}")
print(f"Red alert: {(df['warning_level']=='RED ALERT - Critical Disruption Risk').sum()}")
print(f"Amber: {(df['warning_level']=='AMBER - High Disruption Risk').sum()}")
print(f"Yellow: {(df['warning_level']=='YELLOW - Elevated Disruption Risk').sum()}")
print(f"Green: {(df['warning_level']=='GREEN - Monitor').sum()}")
print(f"Total spend: ${df['total_vendor_spend'].sum():,.0f}")
print(f"Top spend vendor: {df.loc[df['total_vendor_spend'].idxmax(),'vendor_name']} (${df['total_vendor_spend'].max():,.0f})")
print(f"Mean overall resilience: {df['overall_resilience'].mean():.1f}")

# Most common contract expiry cluster
df['expiry_month'] = pd.to_datetime(df['contract_expiry_date']).dt.to_period('M')
print("\nContract expiry distribution:")
print(df.groupby('expiry_month').size().sort_values(ascending=False).head(8))