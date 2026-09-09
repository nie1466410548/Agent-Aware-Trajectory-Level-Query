import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

# ====== Load data for correlation analysis ======
# Monthly high-vol share vs business health score from previous query results
# I'll reconstruct from the query data

# Monthly high-vol share and dashboard data
months_data = [
    ("2024-04", 19.87, 21.42, 80.55, 85.77, 0.4797),
    ("2024-05", 16.31, 16.48, 84.33, 91.20, 0.5552),
    ("2024-06", 9.48, 9.62, 82.93, 84.72, 0.5705),
    ("2024-07", 19.43, 19.06, 84.00, 89.59, 0.5565),
    ("2024-08", 28.68, 28.63, 82.29, 85.04, 0.5392),
    ("2024-09", 33.00, 33.47, 81.49, 85.36, 0.5120),
    ("2024-10", 26.55, 26.93, 82.68, 89.69, 0.5145),
    ("2024-11", 19.46, 18.87, 81.53, 81.53, 0.5529),
    ("2024-12", 7.91, 8.09, 85.27, 91.11, 0.5883),
    ("2025-01", 17.30, 17.67, 84.33, 92.34, 0.5452),
    ("2025-02", 31.66, 32.19, 81.62, 86.18, 0.5099),
    ("2025-03", 31.78, 30.11, 82.44, 87.81, 0.5269),
]

df = pd.DataFrame(months_data, columns=['month', 'hv_rev_share', 'hv_gp_share', 'health_score', 'collection_rate', 'gross_margin'])

print("=== Correlation between HV Share and Business Health Score ===")
r_health, p_health = stats.pearsonr(df['hv_gp_share'], df['health_score'])
print(f"HV Gross Profit Share vs Business Health Score: r={r_health:.4f}, p={p_health:.4f}")

r_coll, p_coll = stats.pearsonr(df['hv_gp_share'], df['collection_rate'])
print(f"HV Gross Profit Share vs Collection Rate: r={r_coll:.4f}, p={p_coll:.4f}")

r_margin, p_margin = stats.pearsonr(df['hv_gp_share'], df['gross_margin'])
print(f"HV Gross Profit Share vs Gross Margin: r={r_margin:.4f}, p={p_margin:.4f}")

# ====== Create visualizations ======
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. HV Share vs Business Health Score
ax1 = axes[0, 0]
ax1.scatter(df['hv_gp_share'], df['health_score'], alpha=0.7, s=80, color='darkred')
z = np.polyfit(df['hv_gp_share'], df['health_score'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['hv_gp_share'].min(), df['hv_gp_share'].max(), 100)
ax1.plot(x_line, p(x_line), '--', color='gray', alpha=0.7)
ax1.set_xlabel('High-Vol Customer Gross Profit Share (%)')
ax1.set_ylabel('Business Health Score')
ax1.set_title(f'Business Health Score vs HV Share\n(r={r_health:.3f}, p={p_health:.3f})')
ax1.grid(True, alpha=0.3)

# 2. HV Share vs Collection Rate
ax2 = axes[0, 1]
ax2.scatter(df['hv_gp_share'], df['collection_rate'], alpha=0.7, s=80, color='darkblue')
z = np.polyfit(df['hv_gp_share'], df['collection_rate'], 1)
p = np.poly1d(z)
ax2.plot(x_line, p(x_line), '--', color='gray', alpha=0.7)
ax2.set_xlabel('High-Vol Customer Gross Profit Share (%)')
ax2.set_ylabel('Collection Rate (%)')
ax2.set_title(f'Collection Rate vs HV Share\n(r={r_coll:.3f}, p={p_coll:.3f})')
ax2.grid(True, alpha=0.3)

# 3. AR Aging Structure Pie Chart
ax3 = axes[1, 0]
ar_labels = ['Current (0-30 days)', 'Past Due (31-60 days)', 'Past Due (61-90 days)', 'Long Overdue (90+ days)']
ar_values = [72.22, 18.06, 7.18, 2.54]
colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
wedges, texts, autotexts = ax3.pie(ar_values, labels=ar_labels, autopct='%1.1f%%', 
                                     colors=colors, startangle=90, explode=(0.03, 0.03, 0.03, 0.08))
ax3.set_title('Accounts Receivable Aging Structure')

# 4. AR Past Due Trend
ax4 = axes[1, 1]
ar_trend = [
    ("2023-12", 28.70), ("2024-01", 30.58), ("2024-02", 34.90), ("2024-03", 33.08),
    ("2024-04", 26.68), ("2024-05", 23.06), ("2024-06", 25.70), ("2024-07", 26.29),
    ("2024-08", 23.50), ("2024-09", 28.13), ("2024-10", 27.83), ("2024-11", 29.76),
    ("2024-12", 28.55), ("2025-01", 28.85), ("2025-02", 27.33), ("2025-03", 27.51),
    ("2025-04", 27.16), ("2025-05", 26.39), ("2025-06", 26.72), ("2025-07", 26.78),
    ("2025-08", 26.72), ("2025-09", 26.82), ("2025-10", 23.79)
]
ar_trend_dates = [t[0] for t in ar_trend]
ar_trend_values = [t[1] for t in ar_trend]
ax4.plot(range(len(ar_trend_dates)), ar_trend_values, 'o-', color='darkorange', linewidth=2)
ax4.axhline(y=28.0, color='red', linestyle='--', alpha=0.5, label='28% Threshold')
ax4.set_xticks(range(0, len(ar_trend_dates), 3))
ax4.set_xticklabels([ar_trend_dates[i] for i in range(0, len(ar_trend_dates), 3)], rotation=45)
ax4.set_xlabel('Date')
ax4.set_ylabel('Past Due % of Total AR')
ax4.set_title('Accounts Receivable Past Due Trend')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig1_correlation_analysis.png', dpi=120, bbox_inches='tight')
plt.close()

print("\nFigure 1 saved: /work/fig1_correlation_analysis.png")

# ====== Multi-dimensional risk model ======
# Build a composite risk score for each customer based on:
# 1. Margin volatility (already ranked)
# 2. Behavioral characteristics (payment behavior, rfm segment)
# 3. Financial risk (outstanding balance ratio, days since last invoice)

# Let me load the customer-level data
print("\n\n=== Multi-dimensional Risk Rating Model ===")

# Define risk scoring weights
# Dimension 1: Volatility risk (from margin_volatility ranking)
# Dimension 2: Payment behavior risk (Poor=4, Average=3, Good=2, Excellent=1)
# Dimension 3: RFM segment risk (At Risk=4, Need Attention=3, others vary)
# Dimension 4: Revenue trend correlation (negative = higher risk)
# Dimension 5: Business stability score (lower = higher risk)

print("Risk Model Dimensions:")
print("1. Margin Volatility - top 25% flagged as high volatility")
print("2. Payment Behavior - Poor (4), Average (3), Good (2), Excellent (1)")
print("3. RFM Segment - At Risk (4), Need Attention (3), others (1-2)")
print("4. Revenue Trend Correlation - negative correlation indicates declining revenue")
print("5. Business Stability Score - lower scores indicate higher risk")
print("6. Collection/Outstanding Ratio - higher outstanding = higher risk")

print("\n=== Key Findings Summary ===")
print(f"Correlation: HV share vs Health Score: r={r_health:.3f}, p={p_health:.3f}")
print(f"Correlation: HV share vs Collection Rate: r={r_coll:.3f}, p={p_coll:.3f}")
print(f"AR Aging: {ar_values[0]:.1f}% Current, {sum(ar_values[1:]):.1f}% Past Due")
print(f"High-Vol customers: 700 out of 2800 (25%)")
print(f"Average CV of monthly gross profit (high-vol): 0.481 (aggregate level)")
print(f"Variance of QoQ invoice_total growth rate (high-vol): 0.401")