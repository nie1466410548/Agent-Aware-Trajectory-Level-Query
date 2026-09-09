import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ====== Figure 2: Risk Tier Distribution by Volatility Segment ======
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Data
segments = ['HighVol', 'MidVol', 'LowVol']
categories = ['High Risk', 'Medium Risk', 'Low Risk']
data = np.array([
    [7.0, 79.4, 13.6],   # HighVol
    [0.9, 54.6, 44.6],   # MidVol
    [0.0, 22.4, 77.6]    # LowVol
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

# ====== Figure 2b: Payment Behavior by Volatility Segment ======
ax = axes[1]
payment_data = {
    'HighVol': [23.0, 26.6, 25.9, 24.6],
    'MidVol': [26.0, 23.3, 23.7, 27.0],
    'LowVol': [20.9, 28.6, 21.9, 28.4]
}
payment_labels = ['Excellent', 'Good', 'Average', 'Poor']
x = np.arange(len(payment_labels))
width = 0.25
colors2 = ['#D32F2F', '#FF9800', '#4CAF50']

for i, (seg, c) in enumerate(zip(['HighVol', 'MidVol', 'LowVol'], colors2)):
    vals = [payment_data[seg][j] for j in range(4)]
    ax.bar(x + i*width, vals, width, label=seg, color=c, alpha=0.75)

ax.set_xticks(x + width)
ax.set_xticklabels(payment_labels)
ax.set_ylabel('Percentage of Segment')
ax.set_title('Payment Behavior Distribution by Volatility Segment')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig2_risk_behavior_profile.png', dpi=120, bbox_inches='tight')
plt.close()
print("Figure 2 saved: /work/fig2_risk_behavior_profile.png")

# ====== Figure 3: Multi-dimensional Risk Rating Framework ======
fig, ax = plt.subplots(figsize=(12, 7))

# Create a radar-like or waterfall chart of the risk model dimensions
dimensions = ['Margin\nVolatility\n(25%)', 'Payment\nBehavior\n(20%)', 'RFM\nSegment\n(20%)', 'Revenue\nTrend\n(15%)', 'Business\nStability\n(20%)']

# Average dimension scores for each risk tier
dim_data = {
    'High Risk': [81.2, 84.1, 86.7, 57.9, 59.8],
    'Medium Risk': [47.5, 48.2, 49.1, 42.3, 52.6],
    'Low Risk': [18.3, 22.1, 18.9, 36.5, 28.4]
}

x = np.arange(len(dimensions))
width = 0.25
colors3 = ['#D32F2F', '#FFC107', '#4CAF50']

for i, (tier, c) in enumerate(zip(dim_data.keys(), colors3)):
    ax.bar(x + i*width, dim_data[tier], width, label=tier, color=c, alpha=0.8)

ax.set_xticks(x + width)
ax.set_xticklabels(dimensions, fontsize=10)
ax.set_ylabel('Average Dimension Score (0-100)')
ax.set_title('Multi-Dimensional Risk Rating Model: Dimension Scores by Risk Tier')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig3_risk_model_dimensions.png', dpi=120, bbox_inches='tight')
plt.close()
print("Figure 3 saved: /work/fig3_risk_model_dimensions.png")

# ====== Figure 4: Profit Stability Comparison ======
fig, ax = plt.subplots(figsize=(10, 6))

metrics = ['CV of Monthly\nGross Profit', 'QoQ Growth\nVariance', 'QoQ Growth\nStd Dev']
hv_values = [0.481, 0.401, 0.633]
lv_values = [0.483, 0.372, 0.610]

x = np.arange(len(metrics))
width = 0.35
ax.bar(x - width/2, hv_values, width, label='High-Volatility Segment', color='#D32F2F', alpha=0.8)
ax.bar(x + width/2, lv_values, width, label='Low-Volatility Segment', color='#4CAF50', alpha=0.8)

ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10)
ax.set_ylabel('Value')
ax.set_title('Profit Stability Metrics: High-Vol vs Low-Vol Segments')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Annotate
for i, (hv, lv) in enumerate(zip(hv_values, lv_values)):
    ax.annotate(f'{hv:.3f}', xy=(i - width/2, hv), ha='center', va='bottom', fontsize=9)
    ax.annotate(f'{lv:.3f}', xy=(i + width/2, lv), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('/work/fig4_profit_stability.png', dpi=120, bbox_inches='tight')
plt.close()
print("Figure 4 saved: /work/fig4_profit_stability.png")

# ====== Figure 5: AR Aging Risk Distribution ======
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
ax = axes[0]
ar_labels = ['Current\n(0-30 days)', 'Past Due\n(31-60 days)', 'Past Due\n(61-90 days)', 'Long Overdue\n(90+ days)']
ar_values = [72.22, 18.06, 7.18, 2.54]
colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
explode = (0.02, 0.03, 0.05, 0.08)
wedges, texts, autotexts = ax.pie(ar_values, labels=ar_labels, autopct='%1.1f%%',
                                   colors=colors, startangle=90, explode=explode,
                                   textprops={'fontsize': 10})
ax.set_title('Accounts Receivable Aging Structure\n(All Periods Aggregate)', fontsize=12, fontweight='bold')

# Bar chart showing past due trend
ax = axes[1]
ar_trend = [
    ("2023-12", 28.70), ("2024-01", 30.58), ("2024-02", 34.90), ("2024-03", 33.08),
    ("2024-04", 26.68), ("2024-05", 23.06), ("2024-06", 25.70), ("2024-07", 26.29),
    ("2024-08", 23.50), ("2024-09", 28.13), ("2024-10", 27.83), ("2024-11", 29.76),
    ("2024-12", 28.55), ("2025-01", 28.85), ("2025-02", 27.33), ("2025-03", 27.51),
    ("2025-04", 27.16), ("2025-05", 26.39), ("2025-06", 26.72), ("2025-07", 26.78),
    ("2025-08", 26.72), ("2025-09", 26.82), ("2025-10", 23.79)
]
dates = [t[0] for t in ar_trend]
values = [t[1] for t in ar_trend]
bars = ax.bar(range(len(dates)), values, color=['#F44336' if v >= 30 else '#FF9800' if v >= 27 else '#FFC107' for v in values])
ax.axhline(y=28.0, color='red', linestyle='--', alpha=0.6, linewidth=1.5, label='28% Threshold')
ax.axhline(y=25.0, color='green', linestyle='--', alpha=0.6, linewidth=1.5, label='25% Target')
ax.set_xticks(range(0, len(dates), 3))
ax.set_xticklabels([dates[i] for i in range(0, len(dates), 3)], rotation=45)
ax.set_xlabel('Date')
ax.set_ylabel('Past Due % of Total AR')
ax.set_title('Accounts Receivable Past Due Trend Over Time', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig5_ar_risk_exposure.png', dpi=120, bbox_inches='tight')
plt.close()
print("Figure 5 saved: /work/fig5_ar_risk_exposure.png")

# ====== Summary statistics ======
print("\n=== Summary Statistics for Report ===")
print(f"High-Volatility Segment: 700 customers (25% of 2800)")
print(f"Threshold (75th percentile): margin_volatility >= 0.237")
print(f"CV of Monthly Gross Profit (High-Vol aggregate): 0.481")
print(f"CV of Monthly Gross Profit (Low-Vol aggregate): 0.483")
print(f"Variance of QoQ Growth (High-Vol): 0.401")
print(f"Variance of QoQ Growth (Low-Vol): 0.372")
print(f"Correlation: HV GP Share vs Business Health Score: r=-0.628, p=0.029")
print(f"Correlation: HV GP Share vs Collection Rate: r=-0.278, p=0.382")
print(f"Correlation: HV GP Share vs Gross Margin: r=-0.741, p=0.006")
print(f"AR Past Due: 27.8% (18.1% + 7.2% + 2.5%)")
print(f"High-Risk Customers (Risk Tier): 61 (2.2%)")
print(f"Medium-Risk: 1477 (52.8%), Low-Risk: 1262 (45.1%)")
print(f"HighVol customers in High Risk tier: 49 (7.0% of HighVol)")
print(f"LowVol customers in High Risk tier: 0 (0%)")