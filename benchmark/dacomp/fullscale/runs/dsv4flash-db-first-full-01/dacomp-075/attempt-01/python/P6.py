import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/risk_warning_results.csv')

# ==========================================
# REFINED ROI MODEL
# ==========================================
# More realistic assumptions:
# - Disruption impact: 15% of annual spend (not 50%) - represents the cost of disruption (finding alternative, production delays, etc.)
# - Business impact multiplier: 2.0 for Critical, 1.5 for High, 1.0 for others
# - 3-year horizon for cost-benefit analysis

impact_mult = {'Critical Impact': 2.0, 'High Impact': 1.5, 'Moderate Impact': 1.2, 'Low Impact': 1.0}
df['impact_multiplier'] = df['business_impact_level'].map(impact_mult).fillna(1.2)

# Annual expected disruption loss (more conservative)
df['expected_annual_loss'] = (df['total_vendor_spend'] * 
                              (df['disruption_probability_12_18mo'] / 100) * 
                              df['impact_multiplier'] * 0.15)  # 15% impact

# STRATEGIES WITH MORE REALISTIC COST/PROB REDUCTION
strategies = {
    'S1: Financial Restructuring': {
        'desc': 'Payment terms renegotiation + early payment program',
        'cost_rate': 0.005,
        'prob_reduction': 0.25,
        'dim': 'financial',
        'payback_years': 1.5
    },
    'S2: Supplier Diversification': {
        'desc': 'Qualify and develop 2+ alternative suppliers',
        'cost_rate': 0.025,
        'prob_reduction': 0.35,
        'dim': 'market',
        'payback_years': 2.0
    },
    'S3: Cybersecurity & Quality Upgrade': {
        'desc': 'Security audit, training, quality improvement program',
        'cost_rate': 0.015,
        'prob_reduction': 0.20,
        'dim': 'operational',
        'payback_years': 2.0
    },
    'S4: Contract Restructuring': {
        'desc': 'Multi-year contract with performance penalties + SLAs',
        'cost_rate': 0.008,
        'prob_reduction': 0.18,
        'dim': 'strategic',
        'payback_years': 1.0
    },
    'S5: Geographic Diversification': {
        'desc': 'Dual-sourcing across regions to reduce concentration',
        'cost_rate': 0.030,
        'prob_reduction': 0.30,
        'dim': 'strategic',
        'payback_years': 3.0
    },
    'S6: Joint Innovation Program': {
        'desc': 'Co-invest in vendor innovation & capability building',
        'cost_rate': 0.012,
        'prob_reduction': 0.15,
        'dim': 'operational',
        'payback_years': 2.5
    },
    'S7: ESG Compliance Program': {
        'desc': 'Environmental sustainability & compliance audits',
        'cost_rate': 0.004,
        'prob_reduction': 0.08,
        'dim': 'strategic',
        'payback_years': 2.0
    },
    'S8: Inventory Buffer & VMI': {
        'desc': 'Vendor-managed inventory + safety stock buffers',
        'cost_rate': 0.020,
        'prob_reduction': 0.40,
        'dim': 'financial',
        'payback_years': 1.0
    },
}

# Compute ROI
roi_results = []
for sname, sinfo in strategies.items():
    annual_cost = df['total_vendor_spend'] * sinfo['cost_rate']
    annual_benefit = df['expected_annual_loss'] * sinfo['prob_reduction']
    
    # 3-year horizon
    total_cost = annual_cost.sum() * 3
    total_benefit = annual_benefit.sum() * 3
    net_benefit = total_benefit - total_cost
    total_roi = net_benefit / total_cost * 100 if total_cost > 0 else 0
    
    # Per-vendor ROI
    per_vendor_roi = (annual_benefit * 3 - annual_cost * 3) / (annual_cost * 3 + 1) * 100
    n_pos = int(np.sum(per_vendor_roi > 0))
    
    roi_results.append({
        'strategy': sname,
        'description': sinfo['desc'],
        'annual_cost': annual_cost.sum(),
        'annual_benefit': annual_benefit.sum(),
        'total_cost_3yr': total_cost,
        'total_benefit_3yr': total_benefit,
        'net_benefit_3yr': net_benefit,
        'roi_pct': total_roi,
        'n_positive_roi': n_pos,
        'payback_years': sinfo['payback_years']
    })

roi_df = pd.DataFrame(roi_results).sort_values('roi_pct', ascending=False)
print("=== REFINED ROI ANALYSIS ===")
print(roi_df[['strategy', 'annual_cost', 'annual_benefit', 'net_benefit_3yr', 'roi_pct', 'n_positive_roi']].round(0).to_string(index=False))

roi_df.to_csv('/work/refined_roi.csv', index=False)

# ==========================================
# FIGURE 9: Refined ROI
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: ROI by strategy
colors = ['#27ae60' if v > 0 else '#e74c3c' for v in roi_df['roi_pct']]
bars = axes[0].barh(roi_df['strategy'].str.replace('S\d+: ', '', regex=True), 
                    roi_df['roi_pct'], color=colors)
axes[0].set_xlabel('ROI (%) - 3-Year Horizon')
axes[0].set_title('Portfolio-wide ROI of Resilience Strategies', fontsize=14, fontweight='bold')
axes[0].axvline(0, color='black', linewidth=1)
for bar, val in zip(bars, roi_df['roi_pct']):
    axes[0].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}%', 
                va='center', fontsize=9, fontweight='bold')

# Right: Net benefit breakdown
benefit_data = roi_df.sort_values('net_benefit_3yr', ascending=True)
axes[1].barh(benefit_data['strategy'].str.replace('S\d+: ', '', regex=True), 
             benefit_data['net_benefit_3yr'], color='steelblue')
axes[1].set_xlabel('Net Benefit ($) - 3-Year Horizon')
axes[1].set_title('Net Financial Benefit of Strategies', fontsize=14, fontweight='bold')
axes[1].axvline(0, color='black', linewidth=1)

plt.tight_layout()
plt.savefig('/work/figure9_refined_roi.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure 9 saved")

# ==========================================
# OPTIMAL STRATEGY PER VENDOR (refined)
# ==========================================
best_strategies = []
for _, row in df.iterrows():
    best_s = None
    best_roi = -np.inf
    for sname, sinfo in strategies.items():
        annual_cost = row['total_vendor_spend'] * sinfo['cost_rate']
        if annual_cost == 0:
            continue
        annual_benefit = row['expected_annual_loss'] * sinfo['prob_reduction']
        roi = (annual_benefit * 3 - annual_cost * 3) / (annual_cost * 3) * 100
        if roi > best_roi:
            best_roi = roi
            best_s = sname
    best_strategies.append({
        'vendor_id': row['vendor_id'],
        'vendor_name': row['vendor_name'],
        'vendor_category': row['vendor_category_name'],
        'best_strategy': best_s,
        'best_roi': best_roi,
        'spend': row['total_vendor_spend'],
        'expected_loss': row['expected_annual_loss'],
        'prob': row['disruption_probability_12_18mo'],
        'resilience_class': row['resilience_class']
    })

best_df = pd.DataFrame(best_strategies)
print(f"\n=== OPTIMAL STRATEGY ASSIGNMENT (Refined) ===")
strat_counts = best_df.groupby('best_strategy')['vendor_name'].count().sort_values(ascending=False)
for s, c in strat_counts.items():
    print(f"  {s}: {c} vendors ({c/len(best_df)*100:.0f}%)")

# For top 20 vendors by spend
top20 = best_df.nlargest(20, 'spend')
print(f"\n=== TOP 20 VENDORS - OPTIMAL STRATEGY ===")
for _, r in top20.iterrows():
    print(f"  {r['vendor_name'][:30]:30s} | ${r['spend']:>8,.0f} | {r['best_strategy'][:30]:30s} | ROI={r['best_roi']:.0f}%")

best_df.to_csv('/work/refined_best_strategy.csv', index=False)

# ==========================================
# PORTFOLIO OPTIMIZATION RECOMMENDATION
# ==========================================
print(f"\n=== PORTFOLIO OPTIMIZATION RECOMMENDATIONS ===")
print(f"Total focus group vendors: {len(df)}")
print(f"Total spend: ${df['total_vendor_spend'].sum():,.0f}")
print(f"Total expected annual disruption loss: ${df['expected_annual_loss'].sum():,.0f}")
print(f"Loss ratio: {df['expected_annual_loss'].sum()/df['total_vendor_spend'].sum()*100:.1f}%")

# Prioritize by risk-adjusted return
df['risk_adjusted_spend'] = df['total_vendor_spend'] * (df['disruption_probability_12_18mo'] / 100) * df['impact_multiplier']
print(f"Risk-adjusted exposure: ${df['risk_adjusted_spend'].sum():,.0f}")

# Contingency plans for each high-risk vendor
print("\n=== CONTINGENCY PLANS FOR KEY HIGH-RISK VENDORS ===")
for _, r in key_high_risk.iterrows():
    best_strat = best_df[best_df['vendor_id'] == r['vendor_id']]['best_strategy'].values
    best_strat = best_strat[0] if len(best_strat) > 0 else 'N/A'
    print(f"\n{r['vendor_name']} (${r['total_vendor_spend']:,.0f})")
    print(f"  Disruption Probability: {r['disruption_probability_12_18mo']:.0f}%")
    print(f"  Recommended Strategy: {best_strat}")
    print(f"  Contingency Plan: ", end="")
    if r['disruption_probability_12_18mo'] >= 70:
        print("IMMEDIATE ACTION: Freeze new orders, activate alternative suppliers, initiate contract renegotiation.")
    elif r['disruption_probability_12_18mo'] >= 60:
        print("SHORT-TERM: Begin alternative supplier qualification, reduce dependency, monitor daily.")
    else:
        print("MONITOR: Regular review, maintain communication, budget for potential disruption.")