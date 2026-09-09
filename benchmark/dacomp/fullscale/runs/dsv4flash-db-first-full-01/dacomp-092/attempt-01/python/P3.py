import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# Exact counts from query S37
# HighVol: Good 186, Average 181, Poor 172, Excellent 161 (total 700)
# MidVol: Poor 378, Excellent 364, Average 332, Good 326 (total 1400)
# LowVol: Good 202, Poor 199, Average 153, Excellent 146 (total 700)

payment_counts = {
    'HighVol': {'Excellent': 161, 'Good': 186, 'Average': 181, 'Poor': 172},
    'MidVol': {'Excellent': 364, 'Good': 326, 'Average': 332, 'Poor': 378},
    'LowVol': {'Excellent': 146, 'Good': 202, 'Average': 153, 'Poor': 199},
}

# Chi-square test between HighVol and LowVol
table = np.array([
    [payment_counts['HighVol']['Excellent'], payment_counts['HighVol']['Good'],
     payment_counts['HighVol']['Average'], payment_counts['HighVol']['Poor']],
    [payment_counts['LowVol']['Excellent'], payment_counts['LowVol']['Good'],
     payment_counts['LowVol']['Average'], payment_counts['LowVol']['Poor']],
])
chi2, p, dof, expected = stats.chi2_contingency(table)
print("=== Chi-square: Volatility (High vs Low) x Payment Behavior ===")
print(f"chi2={chi2:.3f}, p={p:.4f}, dof={dof}")

# Exact percentages
print("\n=== Payment Behavior Percentages ===")
for seg, counts in payment_counts.items():
    total = sum(counts.values())
    pcts = {k: round(100*v/total, 1) for k, v in counts.items()}
    print(f"{seg}: {pcts}")

# ====== RFM segment chi-square ======
rfm_counts = {
    'HighVol': {'Champions': 137, 'New Customers': 128, 'Potential Loyalists': 120,
                'Loyal Customers': 108, 'At Risk': 106, 'Need Attention': 101},
    'LowVol': {'Potential Loyalists': 128, 'Loyal Customers': 128, 'New Customers': 126,
               'Champions': 112, 'At Risk': 109, 'Need Attention': 97},
}
rfm_order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'New Customers', 'Need Attention', 'At Risk']
table_rfm = np.array([
    [rfm_counts['HighVol'][k] for k in rfm_order],
    [rfm_counts['LowVol'][k] for k in rfm_order],
])
chi2r, pr, dofr, expected_r = stats.chi2_contingency(table_rfm)
print("\n=== Chi-square: Volatility (High vs Low) x RFM Segment ===")
print(f"chi2={chi2r:.3f}, p={pr:.4f}, dof={dofr}")

# Regenerate Figure 2 with exact payment percentages
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

segments = ['HighVol', 'MidVol', 'LowVol']
categories = ['High Risk', 'Medium Risk', 'Low Risk']
data = np.array([
    [7.0, 79.4, 13.6],
    [0.9, 54.6, 44.6],
    [0.0, 22.4, 77.6]
])
x = np.arange(len(segments))
width = 0.25
colors = ['#D32F2F', '#FFC107', '#4CAF50']

ax = axes[0]
for i, (cat, c) in enumerate(zip(categories, colors)):
    bars = ax.bar(x + i*width, data[:, i], width, label=cat, color=c, alpha=0.85)
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                       xytext=(0, 5), textcoords="offset points", ha='center', fontsize=9)

ax.set_xticks(x + width)
ax.set_xticklabels(['High Volatility\n(Top 25%)', 'Medium Volatility', 'Low Volatility\n(Bottom 25%)'])
ax.set_ylabel('Percentage of Segment')
ax.set_title('Risk Tier Distribution by Volatility Segment')
ax.legend(loc='upper right')
ax.set_ylim(0, 90)
ax.grid(axis='y', alpha=0.3)

# Payment behavior - exact percentages
pay_pct = {seg: {k: round(100*v/sum(c.values()), 1) for k, v in c.items()} for seg, c in payment_counts.items()}
ax = axes[1]
labels = ['Excellent', 'Good', 'Average', 'Poor']
x = np.arange(4)
width = 0.25
for i, (seg, c) in enumerate(zip(['HighVol', 'MidVol', 'LowVol'], colors)):
    vals = [pay_pct[seg][l] for l in labels]
    bars = ax.bar(x + i*width, vals, width, label=seg, color=c, alpha=0.75)
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                       xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)

ax.set_xticks(x + width)
ax.set_xticklabels(labels)
ax.set_ylabel('Percentage of Segment')
ax.set_title(f'Payment Behavior by Volatility Segment\n(chi-sq p={p:.3f})')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig2_risk_behavior_profile.png', dpi=120, bbox_inches='tight')
plt.close()
print("\nFigure 2 regenerated with exact payment data")

# ====== Also compute revenue share stats for high-vol vs rest ======
# From S55: HighVol outstanding 22156664.83, invoice 8904734.16, collected 20866913.62
# Other: outstanding 77596989.50, invoice 31834590.23, collected 77683308.79
hv_out = 22156664.83
other_out = 77596989.50
total_out = hv_out + other_out
print(f"\n=== Outstanding Balance Contribution ===")
print(f"High-Vol share of outstanding balance: {100*hv_out/total_out:.1f}%")
print(f"High-Vol share of invoices: {100*8904734.16/(8904734.16+31834590.23):.1f}%")
print(f"High-Vol collected/invoice: {20866913.62/8904734.16:.2f}")
print(f"Other collected/invoice: {77683308.79/31834590.23:.2f}")