import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/risk_warning_results.csv')
high_risk = pd.read_csv('/work/high_risk_vendors.csv')

# ==========================================
# PERSONALIZED RESILIENCE IMPROVEMENT PATHS
# ==========================================

# For each high-risk vendor, determine weakest dimensions and recommend actions
def build_improvement_plan(row):
    dims = {
        'Financial': row['financial_resilience'],
        'Operational': row['operational_resilience'],
        'Market': row['market_resilience'],
        'Strategic': row['strategic_resilience']
    }
    weakest = sorted(dims.items(), key=lambda x: x[1])[:2]
    
    recommendations = []
    for dim, score in weakest:
        if dim == 'Financial' and score < 60:
            recommendations.append('Negotiate early-payment discounts; establish dynamic payment terms; set weekly monitoring of overdue AP')
        elif dim == 'Operational' and score < 60:
            recommendations.append('Conduct quality/cybersecurity audit; co-develop innovation roadmap; enforce SLA penalties')
        elif dim == 'Market' and score < 60:
            recommendations.append('Qualify and contract 2+ alternative suppliers; hedge price volatility; build switching playbook')
        elif dim == 'Strategic' and score < 60:
            recommendations.append('Re-negotiate multi-year contract before expiry; diversify geographic sourcing; require ESG compliance')
    
    return '; '.join(recommendations)

# Generate improvement plans for high-risk vendors
high_risk = high_risk.copy()
high_risk['improvement_plan'] = high_risk.apply(build_improvement_plan, axis=1)

# Identify key high-risk vendors (spend > $1M)
key_high_risk = high_risk[high_risk['total_vendor_spend'] > 1000000].sort_values(
    'disruption_probability_12_18mo', ascending=False)

print("=== KEY HIGH-RISK VENDORS (Spend > $1M) - PERSONALIZED PLANS ===")
for _, r in key_high_risk.iterrows():
    print(f"\n--- {r['vendor_name']} ({r['vendor_category_name']}) ---")
    print(f"  Spend: ${r['total_vendor_spend']:,.0f} | Disruption Prob: {r['disruption_probability_12_18mo']:.0f} | Warning: {r['warning_level'][:6]}")
    print(f"  Weakest Dims: Fin={r['financial_resilience']:.0f} Ops={r['operational_resilience']:.0f} Mkt={r['market_resilience']:.0f} Strat={r['strategic_resilience']:.0f}")
    print(f"  Plan: {r['improvement_plan']}")

key_high_risk.to_csv('/work/key_high_risk_vendors_plans.csv', index=False)
print(f"\nSaved {len(key_high_risk)} key high-risk vendor plans")

# ==========================================
# ROI ANALYSIS OF IMPROVEMENT STRATEGIES
# ==========================================

# Business impact multiplier by impact level
impact_mult = {'Critical Impact': 3.0, 'High Impact': 2.0, 'Moderate Impact': 1.5, 'Low Impact': 1.0}
df['impact_multiplier'] = df['business_impact_level'].map(impact_mult).fillna(1.5)

# Expected annual disruption loss = spend * disruption_probability/100 * impact_multiplier * 0.5
# (assume disruption causes ~50% of annual spend impact on average)
df['expected_annual_loss'] = (df['total_vendor_spend'] * 
                              (df['disruption_probability_12_18mo'] / 100) * 
                              df['impact_multiplier'] * 0.5)

# STRATEGY DEFINITIONS
strategies = {
    'S1: Financial Restructuring': {
        'desc': 'Payment terms renegotiation + early payment program',
        'cost_rate': 0.005,  # 0.5% of spend
        'prob_reduction': 0.25,  # reduces disruption probability by 25%
        'dim': 'financial'
    },
    'S2: Supplier Diversification': {
        'desc': 'Qualify and develop 2+ alternative suppliers',
        'cost_rate': 0.02,  # 2% of spend
        'prob_reduction': 0.30,
        'dim': 'market'
    },
    'S3: Cybersecurity & Quality Upgrade': {
        'desc': 'Security audit, training, quality improvement program',
        'cost_rate': 0.015,
        'prob_reduction': 0.20,
        'dim': 'operational'
    },
    'S4: Contract Restructuring': {
        'desc': 'Multi-year contract with performance penalties + SLAs',
        'cost_rate': 0.008,
        'prob_reduction': 0.20,
        'dim': 'strategic'
    },
    'S5: Geographic Diversification': {
        'desc': 'Dual-sourcing across regions to reduce concentration',
        'cost_rate': 0.025,
        'prob_reduction': 0.25,
        'dim': 'strategic'
    },
    'S6: Joint Innovation Program': {
        'desc': 'Co-invest in vendor innovation & capability building',
        'cost_rate': 0.012,
        'prob_reduction': 0.15,
        'dim': 'operational'
    },
    'S7: ESG Compliance Program': {
        'desc': 'Environmental sustainability & compliance audits',
        'cost_rate': 0.004,
        'prob_reduction': 0.10,
        'dim': 'strategic'
    },
    'S8: Inventory Buffer & VMI': {
        'desc': 'Vendor-managed inventory + safety stock buffers',
        'cost_rate': 0.018,
        'prob_reduction': 0.35,
        'dim': 'financial'
    },
}

# Compute ROI per strategy per vendor
roi_results = []
for sname, sinfo in strategies.items():
    cost = df['total_vendor_spend'] * sinfo['cost_rate']
    # Benefit = reduction in expected annual loss over 3-year horizon
    benefit = df['expected_annual_loss'] * sinfo['prob_reduction'] * 3  # 3-year benefit
    net_benefit = benefit - cost
    roi = np.where(cost > 0, net_benefit / cost * 100, 0)
    
    roi_results.append({
        'strategy': sname,
        'description': sinfo['desc'],
        'total_cost': cost.sum(),
        'total_benefit_3yr': benefit.sum(),
        'total_net_benefit': net_benefit.sum(),
        'total_roi_pct': net_benefit.sum() / cost.sum() * 100 if cost.sum() > 0 else 0,
        'avg_roi_pct': np.mean(roi),
        'median_roi_pct': np.median(roi),
        'n_positive_roi': int(np.sum(roi > 0))
    })

roi_df = pd.DataFrame(roi_results).sort_values('total_roi_pct', ascending=False)
print("\n=== ROI ANALYSIS OF RESILIENCE IMPROVEMENT STRATEGIES ===")
print(roi_df[['strategy', 'total_cost', 'total_benefit_3yr', 'total_net_benefit', 'total_roi_pct', 'n_positive_roi']].round(0).to_string(index=False))

roi_df.to_csv('/work/roi_analysis.csv', index=False)

# ==========================================
# FIGURE 7: ROI comparison
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(roi_df['strategy'].str.replace('S\d+: ', '', regex=True), 
               roi_df['total_roi_pct'], 
               color=['#27ae60' if v > 0 else '#e74c3c' for v in roi_df['total_roi_pct']])
ax.set_xlabel('ROI (% over 3 years)')
ax.set_title('ROI of Resilience Improvement Strategies (Portfolio-wide, 3-Year Horizon)', 
             fontsize=14, fontweight='bold')
ax.axvline(0, color='black', linewidth=1)
for bar, val in zip(bars, roi_df['total_roi_pct']):
    ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.0f}%', 
            va='center', fontsize=10, fontweight='bold')
ax.set_xlim(min(roi_df['total_roi_pct']) - 50, max(roi_df['total_roi_pct']) + 50)
plt.tight_layout()
plt.savefig('/work/figure7_roi_strategies.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigure 7 saved")

# ==========================================
# FIGURE 8: Optimal strategy per vendor
# ==========================================
# For each vendor, pick the best strategy by ROI
best_strategies = []
for _, row in df.iterrows():
    best_s = None
    best_roi = -np.inf
    for sname, sinfo in strategies.items():
        cost = row['total_vendor_spend'] * sinfo['cost_rate']
        if cost == 0:
            continue
        benefit = row['expected_annual_loss'] * sinfo['prob_reduction'] * 3
        roi = (benefit - cost) / cost * 100
        if roi > best_roi:
            best_roi = roi
            best_s = sname
    best_strategies.append({'vendor_id': row['vendor_id'], 'vendor_name': row['vendor_name'],
                            'best_strategy': best_s, 'best_roi': best_roi,
                            'spend': row['total_vendor_spend'],
                            'expected_loss': row['expected_annual_loss'],
                            'prob': row['disruption_probability_12_18mo']})

best_df = pd.DataFrame(best_strategies)
print("\n=== OPTIMAL STRATEGY ASSIGNMENT ===")
print(best_df.groupby('best_strategy')['vendor_name'].count().sort_values(ascending=False))
best_df.to_csv('/work/best_strategy_per_vendor.csv', index=False)

# Figure 8: best strategy allocation for top spend vendors
top20 = best_df.nlargest(20, 'spend')
fig, ax = plt.subplots(figsize=(14, 6))
colors = plt.cm.tab20(np.linspace(0, 1, 8))
strat_color = {s: colors[i] for i, s in enumerate(sorted(best_df['best_strategy'].unique()))}
bars = ax.barh(top20['vendor_name'].str[:25], top20['best_roi'], 
               color=[strat_color[s] for s in top20['best_strategy']])
ax.set_xlabel('Best Strategy ROI (%)')
ax.set_title('Optimal Resilience Strategy ROI by Top-Spend Vendor', fontsize=14, fontweight='bold')
ax.axvline(0, color='black', linewidth=1)
# Legend
handles = [plt.Rectangle((0,0),1,1, color=strat_color[s]) for s in sorted(best_df['best_strategy'].unique())]
ax.legend(handles, [s.split(': ')[1] for s in sorted(best_df['best_strategy'].unique())], 
          loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig('/work/figure8_best_strategy_roi.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigure 8 saved")

# Total portfolio exposure
total_spend = df['total_vendor_spend'].sum()
total_expected_loss = df['expected_annual_loss'].sum()
print(f"\n=== PORTFOLIO SUMMARY ===")
print(f"Total focus-group spend: ${total_spend:,.0f}")
print(f"Total expected annual disruption loss: ${total_expected_loss:,.0f}")
print(f"Expected loss as % of spend: {total_expected_loss/total_spend*100:.1f}%")