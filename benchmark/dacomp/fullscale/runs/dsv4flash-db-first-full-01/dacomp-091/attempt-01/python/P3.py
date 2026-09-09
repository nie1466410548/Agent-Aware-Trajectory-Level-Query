import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ============ VENDOR DATA ============
r1 = db.query("""
  SELECT vendor_id, vendor_display_name, annual_spend_growth_pct, overall_performance_score,
         spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score,
         avg_monthly_spend
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
""")
df_v = db.frame(r1)
df_v['vol_coef'] = df_v['spend_volatility'] / df_v['total_lifetime_spend'].replace(0, np.nan)
df_v['comp_risk'] = df_v['payment_completion_rate']*0.4 + df_v['business_value_score']/10.0*0.6

# ============ ACCOUNT TYPE DATA ============
r2 = db.query("""
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
  ORDER BY account_type
""")
df_acct = db.frame(r2)

# ============ CASH FLOW DATA ============
r3 = db.query("""
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
df_cf = db.frame(r3)
df_cf['forecast_month'] = pd.to_datetime(df_cf['forecast_month'])
df_cf['month_label'] = df_cf['forecast_month'].dt.strftime('%Y-%m')
df_cf['cum_baseline_net'] = df_cf['forecasted_net_cash_flow'].cumsum()
df_cf['cum_adjusted_net'] = df_cf['adjusted_net'].cumsum()
df_cf['baseline_lri'] = df_cf['forecasted_net_cash_flow'].apply(lambda x: max(0, -x) / 1 if x < 0 else 0)
# monthly deficit ratios need inflows
df_cf['baseline_lri'] = np.where(df_cf['forecasted_net_cash_flow'] < 0,
                                 -df_cf['forecasted_net_cash_flow']/df_cf['forecasted_inflows'], 0)
df_cf['adjusted_lri'] = np.where(df_cf['adjusted_net'] < 0,
                                 -df_cf['adjusted_net']/df_cf['forecasted_inflows'], 0)

# ============ FIGURE 1: Vendor metrics ============
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0][0]
ax1.hist(df_v['vol_coef'], bins=30, color='steelblue', edgecolor='white', alpha=0.8)
ax1.axvline(df_v['vol_coef'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_v["vol_coef"].mean():.4f}')
ax1.set_xlabel('Spend Volatility Coefficient (spend_volatility / lifetime spend)')
ax1.set_ylabel('Number of Vendors')
ax1.set_title('(a) Spend Volatility Coefficient Distribution')
ax1.legend()

ax2 = axes[0][1]
ax2.hist(df_v['comp_risk'], bins=30, color='darkorange', edgecolor='white', alpha=0.8)
ax2.axvline(df_v['comp_risk'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_v["comp_risk"].mean():.4f}')
ax2.set_xlabel('Composite Risk Score (payment_completion*0.4 + value/10*0.6)')
ax2.set_ylabel('Number of Vendors')
ax2.set_title('(b) Composite Risk Score Distribution')
ax2.legend()

ax3 = axes[1][0]
sc = ax3.scatter(df_v['annual_spend_growth_pct'], df_v['overall_performance_score'], c=df_v['comp_risk'],
                 cmap='RdYlGn_r', s=25, alpha=0.6, edgecolors='grey', linewidth=0.5)
cb = plt.colorbar(sc, ax=ax3)
cb.set_label('Composite Risk Score')
ax3.set_xlabel('Annual Spend Growth (%)')
ax3.set_ylabel('Overall Performance Score')
ax3.set_title('(c) Growth vs Performance (colored by composite risk)')

ax4 = axes[1][1]
top20 = df_v.nlargest(20, 'total_lifetime_spend')
ax4.barh(range(len(top20)), top20['total_lifetime_spend'].values/1000, color='teal', alpha=0.7)
ax4.set_yticks(range(len(top20)))
ax4.set_yticklabels(top20['vendor_display_name'].values, fontsize=8)
ax4.set_xlabel('Total Lifetime Spend ($K)')
ax4.set_title('(d) Top 20 Shrinking-Spend High-Quality Vendors by Lifetime Spend')
ax4.invert_yaxis()

plt.tight_layout()
plt.savefig('fig1_vendor_metrics.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig1 saved")

# ============ FIGURE 2: Account type ============
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

ax1 = axes[0]
accts = df_acct['account_type'].values
changes = df_acct['avg_change'].values
colors = ['#2ecc71' if c > 0 else '#e74c3c' for c in changes]
ax1.bar(accts, changes, color=colors, alpha=0.8, edgecolor='grey', linewidth=0.5)
ax1.axhline(0, color='black', linewidth=0.8)
for i, (a, c) in enumerate(zip(accts, changes)):
    ax1.text(i, c + (5 if c >= 0 else -8), f'{c:.1f}%', ha='center',
             va='bottom' if c >= 0 else 'top', fontsize=9, fontweight='bold')
ax1.set_ylabel('Avg Spend Change Rate (%)')
ax1.set_title('(a) Avg Spend Change Rate by Account Type\n(Last 12M vs Prior 12M, per vendor-account pair)')

ax2 = axes[1]
freqs = df_acct['avg_freq'].values
ax2.bar(accts, freqs, color='#8e44ad', alpha=0.8, edgecolor='grey', linewidth=0.5)
for i, (a, f) in enumerate(zip(accts, freqs)):
    ax2.text(i, f + 0.002, f'{f:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_ylabel('Avg Transaction Frequency Density\n(Transactions / Active Days)')
ax2.set_title('(b) Transaction Frequency Density by Account Type')

plt.tight_layout()
plt.savefig('fig2_account_type_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig2 saved")

# ============ FIGURE 3: Cash flow impact ============
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
x = np.arange(len(df_cf))
w = 0.35

ax1 = axes[0][0]
ax1.bar(x - w/2, df_cf['forecasted_outflows'].values/1e6, w, label='Baseline Outflow', color='#c0392b', alpha=0.85)
ax1.bar(x + w/2, df_cf['adjusted_outflow'].values/1e6, w, label='Adjusted Outflow', color='#27ae60', alpha=0.85)
ax1.set_xticks(x)
ax1.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Monthly Outflow ($M)')
ax1.set_title('(a) Monthly Outflow Forecast: Baseline vs Adjusted')
ax1.legend()

ax2 = axes[0][1]
ax2.plot(x, df_cf['forecasted_net_cash_flow'].values/1e6, 'o-', color='#c0392b', linewidth=2, markersize=6, label='Baseline Net CF')
ax2.plot(x, df_cf['adjusted_net'].values/1e6, 's-', color='#27ae60', linewidth=2, markersize=6, label='Adjusted Net CF')
ax2.axhline(0, color='black', linewidth=0.8, alpha=0.5)
ax2.fill_between(x, df_cf['adjusted_net'].values/1e6, df_cf['forecasted_net_cash_flow'].values/1e6,
                 alpha=0.2, color='green')
ax2.set_xticks(x)
ax2.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax2.set_ylabel('Net Cash Flow ($M)')
ax2.set_title('(b) Monthly Net Cash Flow: Baseline vs Adjusted')
ax2.legend()

ax3 = axes[1][0]
ax3.plot(x, df_cf['cum_baseline_net'].values/1e6, 'o-', color='#c0392b', linewidth=2, markersize=6, label='Baseline Cumulative')
ax3.plot(x, df_cf['cum_adjusted_net'].values/1e6, 's-', color='#27ae60', linewidth=2, markersize=6, label='Adjusted Cumulative')
ax3.fill_between(x, df_cf['cum_adjusted_net'].values/1e6, df_cf['cum_baseline_net'].values/1e6,
                 alpha=0.2, color='green')
ax3.axhline(0, color='black', linewidth=0.8, alpha=0.5)
ax3.set_xticks(x)
ax3.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax3.set_ylabel('Cumulative Net Cash Flow ($M)')
ax3.set_title('(c) Cumulative Net Cash Flow Trajectory')
ax3.legend()

ax4 = axes[1][1]
ax4.bar(x, df_cf['vendor_reduction'].values/1e3, color='#2980b9', alpha=0.85, edgecolor='white')
ax4.set_xticks(x)
ax4.set_xticklabels(df_cf['month_label'].values, rotation=45, ha='right', fontsize=8)
ax4.set_ylabel('Cash Flow Improvement ($K)')
ax4.set_title('(d) Monthly Cash Flow Improvement from 30% Vendor Reduction')
ax4.text(0.5, 0.95, f'Total 18-Month Improvement: ${df_cf["vendor_reduction"].sum():,.0f}',
         transform=ax4.transAxes, ha='center', va='top', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('fig3_cash_flow_impact.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig3 saved")

# Print summaries
print(f"N vendors: {len(df_v)}")
print(f"Vol coef: mean={df_v['vol_coef'].mean():.6f}, median={df_v['vol_coef'].median():.6f}, min={df_v['vol_coef'].min():.6f}, max={df_v['vol_coef'].max():.6f}")
print(f"Comp risk: mean={df_v['comp_risk'].mean():.6f}, min={df_v['comp_risk'].min():.6f}, max={df_v['comp_risk'].max():.6f}")
print(f"Total lifetime spend: {df_v['total_lifetime_spend'].sum():,.2f}")
print(f"Total avg monthly spend: {df_v['avg_monthly_spend'].sum():,.2f}")
print(df_acct)
print(df_cf[['month_label','forecasted_outflows','adjusted_outflow','vendor_reduction','forecasted_net_cash_flow','adjusted_net','baseline_lri','adjusted_lri']].round(2))
print(f"Total baseline outflow: {df_cf['forecasted_outflows'].sum():,.2f}")
print(f"Total adjusted outflow: {df_cf['adjusted_outflow'].sum():,.2f}")
print(f"Total reduction: {df_cf['vendor_reduction'].sum():,.2f}")
print(f"Baseline cum net final: {df_cf['cum_baseline_net'].iloc[-1]:,.2f}")
print(f"Adjusted cum net final: {df_cf['cum_adjusted_net'].iloc[-1]:,.2f}")
print(f"Baseline avg LRI: {df_cf['baseline_lri'].mean():.6f}")
print(f"Adjusted avg LRI: {df_cf['adjusted_lri'].mean():.6f}")
print(f"LRI change: {df_cf['baseline_lri'].mean() - df_cf['adjusted_lri'].mean():.6f}")