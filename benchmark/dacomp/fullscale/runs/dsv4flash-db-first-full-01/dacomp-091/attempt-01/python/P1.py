import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import json, os

# Load data
# Vendor performance data for the 342 selected vendors
rows = db.query("SELECT vendor_id, annual_spend_growth_pct, overall_performance_score, spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score, avg_monthly_spend, spend_current_year, spend_prev_year, vendor_display_name FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7")
vendors = []
for r in db.rows(rows):
    sv = r['spend_volatility'] / r['total_lifetime_spend'] if r['total_lifetime_spend'] else 0
    cr = r['payment_completion_rate']*0.4 + r['business_value_score']/10.0*0.6
    vendors.append({
        'vid': r['vendor_id'],
        'name': r['vendor_display_name'],
        'growth': r['annual_spend_growth_pct'],
        'score': r['overall_performance_score'],
        'vol_coef': sv,
        'comp_risk': cr,
        'avg_monthly': r['avg_monthly_spend'],
        'lifetime': r['total_lifetime_spend'],
        'spend_cy': r['spend_current_year'],
        'spend_py': r['spend_prev_year']
    })

df_v = pd.DataFrame(vendors)

# Load account-type spend change data
rows2 = db.query("""
  SELECT account_type,
    AVG(spend_change_rate_pct) as avg_change,
    AVG(tx_frequency_density) as avg_freq,
    SUM(spend_last12) as total_last12,
    SUM(spend_prior12) as total_prior12
  FROM (
    SELECT vendor_id, account_type,
      SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
      SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
      CASE WHEN ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
        THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) - SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))
             / ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) * 100
        ELSE NULL END AS spend_change_rate_pct,
      COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
    FROM quickbooks__general_ledger
    WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
    GROUP BY vendor_id, account_type
  ) t
  GROUP BY account_type
""")
df_acct = pd.DataFrame(db.rows(rows2))

# Cash flow forecast data
rows3 = db.query("""
  WITH vendor_share AS (SELECT 0.2318 AS outflow_share)
  SELECT
    forecast_month,
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) AS adjusted_net,
    cash_flow_health_score,
    liquidity_risk_level
  FROM quickbooks__cashflow_forecast, vendor_share
  ORDER BY forecast_month
""")
df_cf = pd.DataFrame(db.rows(rows3))
df_cf['forecast_month'] = pd.to_datetime(df_cf['forecast_month'])
df_cf['month_label'] = df_cf['forecast_month'].dt.strftime('%Y-%m')

# Compute cumulative
df_cf['cum_baseline_net'] = df_cf['forecasted_net_cash_flow'].cumsum()
df_cf['cum_adjusted_net'] = df_cf['adjusted_net'].cumsum()

# ======== FIGURE 1: Vendor metrics distribution ========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Spend volatility coefficient
ax1 = axes[0][0]
ax1.hist(df_v['vol_coef'], bins=30, color='steelblue', edgecolor='white', alpha=0.8)
ax1.axvline(df_v['vol_coef'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_v["vol_coef"].mean():.4f}')
ax1.set_xlabel('Spend Volatility Coefficient')
ax1.set_ylabel('Number of Vendors')
ax1.set_title('(a) Spend Volatility Coefficient Distribution')
ax1.legend()

# Composite risk score
ax2 = axes[0][1]
ax2.hist(df_v['comp_risk'], bins=30, color='darkorange', edgecolor='white', alpha=0.8)
ax2.axvline(df_v['comp_risk'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_v["comp_risk"].mean():.4f}')
ax2.set_xlabel('Composite Risk Score')
ax2.set_ylabel('Number of Vendors')
ax2.set_title('(b) Composite Risk Score Distribution')
ax2.legend()

# Annual spend growth vs performance score
ax3 = axes[1][0]
scatter = ax3.scatter(df_v['growth'], df_v['score'], c=df_v['comp_risk'], 
                       cmap='RdYlGn_r', s=30, alpha=0.6, edgecolors='grey', linewidth=0.5)
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('Composite Risk Score')
ax3.set_xlabel('Annual Spend Growth (%)')
ax3.set_ylabel('Overall Performance Score')
ax3.set_title('(c) Growth vs Performance (colored by Risk)')

# Top 20 vendors by lifetime spend
ax4 = axes[1][1]
top20 = df_v.nlargest(20, 'lifetime')
bars = ax4.barh(range(len(top20)), top20['lifetime'].values, color='teal', alpha=0.7)
ax4.set_yticks(range(len(top20)))
ax4.set_yticklabels(top20['name'].values, fontsize=8)
ax4.set_xlabel('Total Lifetime Spend ($)')
ax4.set_title('(d) Top 20 Vendors by Lifetime Spend')
ax4.invert_yaxis()
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('/work/fig1_vendor_metrics.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved")

# ======== FIGURE 2: Account-type spend analysis ========
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

ax1 = axes[0]
accts = df_acct['account_type'].values
changes = df_acct['avg_change'].values
colors = ['#2ecc71' if c > 0 else '#e74c3c' for c in changes]
bars = ax1.bar(accts, changes, color=colors, alpha=0.8, edgecolor='grey', linewidth=0.5)
ax1.axhline(0, color='black', linewidth=0.8)
for i, (a, c) in enumerate(zip(accts, changes)):
    ax1.text(i, c + (5 if c >= 0 else -5), f'{c:.1f}%', ha='center', va='bottom' if c >= 0 else 'top', fontsize=9, fontweight='bold')
ax1.set_ylabel('Avg Spend Change Rate (%)')
ax1.set_title('(a) Avg Spend Change Rate by Account Type\n(Last 12M vs Prior 12M)')
ax1.tick_params(axis='x', rotation=0)

# Frequency density
ax2 = axes[1]
freqs = df_acct['avg_freq'].values
bars2 = ax2.bar(accts, freqs, color='#8e44ad', alpha=0.8, edgecolor='grey', linewidth=0.5)
for i, (a, f) in enumerate(zip(accts, freqs)):
    ax2.text(i, f + 0.002, f'{f:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_ylabel('Avg Transaction Frequency Density\n(Transactions / Active Days)')
ax2.set_title('(b) Transaction Frequency Density by Account Type')
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('/work/fig2_account_type_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved")

# ======== FIGURE 3: Cash flow impact model ========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Monthly outflows
ax1 = axes[0][0]
x = np.arange(len(df_cf))
w = 0.35
bars1 = ax1.bar(x - w/2, df_cf['forecasted_outflows'].values/1e6, w, label='Baseline Outflow', color='#c0392b', alpha=0.8)
bars2 = ax1.bar(x + w/2, df_cf['adjusted_outflow'].values/1e6, w, label='Adjusted Outflow (-30% vendor)', color='#27ae60', alpha=0.8)
ax1.set_xticks(x)
ax1.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Monthly Outflow ($M)')
ax1.set_title('(a) Monthly Outflow: Baseline vs Adjusted')
ax1.legend()
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}M'))

# Net cash flow
ax2 = axes[0][1]
ax2.plot(x, df_cf['forecasted_net_cash_flow'].values/1e6, 'o-', color='#c0392b', linewidth=2, markersize=6, label='Baseline Net CF')
ax2.plot(x, df_cf['adjusted_net'].values/1e6, 's-', color='#27ae60', linewidth=2, markersize=6, label='Adjusted Net CF')
ax2.axhline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)
ax2.fill_between(x, df_cf['adjusted_net'].values/1e6, df_cf['forecasted_net_cash_flow'].values/1e6, 
                  alpha=0.2, color='green', label='Improvement')
ax2.set_xticks(x)
ax2.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax2.set_ylabel('Net Cash Flow ($M)')
ax2.set_title('(b) Monthly Net Cash Flow: Baseline vs Adjusted')
ax2.legend()
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}M'))

# Cumulative net cash flow
ax3 = axes[1][0]
ax3.plot(x, df_cf['cum_baseline_net'].values/1e6, 'o-', color='#c0392b', linewidth=2, markersize=6, label='Baseline Cumulative')
ax3.plot(x, df_cf['cum_adjusted_net'].values/1e6, 's-', color='#27ae60', linewidth=2, markersize=6, label='Adjusted Cumulative')
ax3.fill_between(x, df_cf['cum_adjusted_net'].values/1e6, df_cf['cum_baseline_net'].values/1e6, 
                  alpha=0.2, color='green', label='Cumulative Improvement')
ax3.axhline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)
ax3.set_xticks(x)
ax3.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax3.set_ylabel('Cumulative Net Cash Flow ($M)')
ax3.set_title('(c) Cumulative Net Cash Flow Trajectory')
ax3.legend()
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}M'))

# Vendor reduction amounts
ax4 = axes[1][1]
ax4.bar(x, df_cf['vendor_reduction'].values/1e3, color='#2980b9', alpha=0.8, edgecolor='white')
ax4.set_xticks(x)
ax4.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax4.set_ylabel('Cash Flow Improvement ($K)')
ax4.set_title('(d) Monthly Cash Flow Improvement from 30% Vendor Reduction')
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.0f}K'))

# Add total reduction annotation
total_reduction = df_cf['vendor_reduction'].sum()
ax4.text(0.5, 0.95, f'Total 18-Month Improvement: ${total_reduction:,.0f}', 
         transform=ax4.transAxes, ha='center', va='top', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('/work/fig3_cash_flow_impact.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved")

# Summary statistics
print("=== Vendor Summary ===")
print(f"Number of high-quality, shrinking-spend vendors: {len(df_v)}")
print(f"Avg spend volatility coefficient: {df_v['vol_coef'].mean():.6f}")
print(f"Avg composite risk score: {df_v['comp_risk'].mean():.6f}")
print(f"Total lifetime spend: ${df_v['lifetime'].sum():,.2f}")
print(f"Total avg monthly spend: ${df_v['avg_monthly'].sum():,.2f}")

print("\n=== Account Type Summary ===")
for _, r in df_acct.iterrows():
    print(f"{r['account_type']}: avg_change={r['avg_change']:.2f}%, avg_freq={r['avg_freq']:.4f}")

print("\n=== Cash Flow Impact Summary ===")
print(f"Total baseline outflow (18 months): ${df_cf['forecasted_outflows'].sum():,.2f}")
print(f"Total adjusted outflow: ${df_cf['adjusted_outflow'].sum():,.2f}")
print(f"Total vendor reduction: ${df_cf['vendor_reduction'].sum():,.2f}")
print(f"Baseline cumulative net: ${df_cf['cum_baseline_net'].iloc[-1]:,.2f}")
print(f"Adjusted cumulative net: ${df_cf['cum_adjusted_net'].iloc[-1]:,.2f}")
print(f"Baseline avg LRI: {df_cf['forecasted_net_cash_flow'].apply(lambda x: max(0, -x) if x < 0 else 0).mean():.6f}")