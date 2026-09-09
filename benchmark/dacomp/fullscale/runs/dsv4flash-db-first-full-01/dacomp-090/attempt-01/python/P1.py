import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy.stats import mannwhitneyu, pearsonr

# 1. Load data for high-risk vs normal comparison
df_all = db.frame(db.query("""
  SELECT customer_id, customer_lifespan_days, total_invoices, avg_invoice_amount,
         credit_score, business_stability_score, outstanding_balance, payment_rate_percentage,
         overdue_count_12m, avg_payment_days_12m, days_since_last_invoice, revenue_growth_rate_12m,
         active_months, total_invoice_amount, monthly_revenue_avg, payment_timeliness_score,
         total_payments, unique_products_purchased, revenue_growth_yoy_pct,
         CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
"""))

print("Total rows:", len(df_all))
print("High-Risk:", (df_all['risk_group']=='High-Risk').sum())
print("Normal:", (df_all['risk_group']=='Normal').sum())

# 2. Statistical tests
numeric_cols = ['customer_lifespan_days', 'total_invoices', 'avg_invoice_amount',
                'credit_score', 'business_stability_score', 'outstanding_balance',
                'payment_rate_percentage', 'overdue_count_12m', 'avg_payment_days_12m',
                'days_since_last_invoice', 'revenue_growth_rate_12m', 'active_months',
                'total_invoice_amount', 'monthly_revenue_avg', 'payment_timeliness_score',
                'total_payments', 'unique_products_purchased']

results = []
for col in numeric_cols:
    hr = df_all[df_all['risk_group']=='High-Risk'][col].dropna()
    nm = df_all[df_all['risk_group']=='Normal'][col].dropna()
    stat, pval = mannwhitneyu(hr, nm, alternative='two-sided')
    results.append({
        'metric': col,
        'high_risk_mean': round(hr.mean(), 2),
        'normal_mean': round(nm.mean(), 2),
        'diff_pct': round((hr.mean() - nm.mean()) / abs(nm.mean()) * 100, 2),
        'mannwhitney_u': stat,
        'p_value': pval,
        'significant': 'Yes' if pval < 0.05 else 'No'
    })

df_stats = pd.DataFrame(results)
df_stats = df_stats.sort_values('p_value')
print("\n===== Statistical Comparison (Mann-Whitney U) =====")
print(df_stats.to_string(index=False))

# 3. Visualization: Risk Score Distribution
df_risk = db.frame(db.query("""
  SELECT customer_id, outstanding_balance,
    (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
"""))

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# A: Risk score histogram
axes[0,0].hist(df_risk['risk_score'], bins=20, color='crimson', edgecolor='white', alpha=0.8)
axes[0,0].axvline(df_risk['risk_score'].mean(), color='darkblue', linestyle='--', linewidth=2, label=f'Mean={df_risk["risk_score"].mean():.1f}')
axes[0,0].set_xlabel('Composite Risk Score')
axes[0,0].set_ylabel('Number of Customers')
axes[0,0].set_title('High-Risk Customer Risk Score Distribution')
axes[0,0].legend()
axes[0,0].grid(axis='y', alpha=0.3)

# B: Risk score vs outstanding balance scatter
axes[0,1].scatter(df_risk['risk_score'], df_risk['outstanding_balance'], alpha=0.5, c='darkred', s=30)
axes[0,1].set_xlabel('Risk Score')
axes[0,1].set_ylabel('Outstanding Balance ($)')
axes[0,1].set_title('Risk Score vs Outstanding Balance')
axes[0,1].grid(alpha=0.3)

# C: Boxplot comparison - customer_lifespan_days
sns.boxplot(x='risk_group', y='customer_lifespan_days', data=df_all, ax=axes[0,2], palette=['crimson','steelblue'])
axes[0,2].set_title('Customer Lifespan Days')
axes[0,2].set_xlabel('')

# D: Boxplot comparison - total_invoices
sns.boxplot(x='risk_group', y='total_invoices', data=df_all, ax=axes[1,0], palette=['crimson','steelblue'])
axes[1,0].set_title('Total Invoices')
axes[1,0].set_xlabel('')

# E: Boxplot comparison - avg_invoice_amount
sns.boxplot(x='risk_group', y='avg_invoice_amount', data=df_all, ax=axes[1,1], palette=['crimson','steelblue'])
axes[1,1].set_title('Avg Invoice Amount ($)')
axes[1,1].set_xlabel('')

# F: Boxplot - credit_score
sns.boxplot(x='risk_group', y='credit_score', data=df_all, ax=axes[1,2], palette=['crimson','steelblue'])
axes[1,2].set_title('Credit Score')
axes[1,2].set_xlabel('')

plt.tight_layout()
plt.savefig('/work/risk_analysis_1.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved risk_analysis_1.png")

# 4. Collection rate trend visualization
df_fin = db.frame(db.query("""
  SELECT dashboard_month, collection_rate_percentage, outstanding_receivables, overdue_amount, gross_profit
  FROM quickbooks__financial_dashboard
  ORDER BY dashboard_month
"""))
df_fin['dashboard_month'] = pd.to_datetime(df_fin['dashboard_month'])

# Last 12 months
df_fin_last12 = df_fin.tail(12).copy()
df_fin_last12['mom_change'] = df_fin_last12['collection_rate_percentage'].diff()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Full collection rate trend
ax1.plot(df_fin['dashboard_month'], df_fin['collection_rate_percentage'], 
         marker='o', color='steelblue', linewidth=2, markersize=5)
ax1.axhline(df_fin['collection_rate_percentage'].mean(), color='gray', linestyle='--', 
            label=f'Overall Mean: {df_fin["collection_rate_percentage"].mean():.1f}%')
ax1.fill_between(df_fin['dashboard_month'], df_fin['collection_rate_percentage'], 
                 df_fin['collection_rate_percentage'].mean(), alpha=0.15, color='steelblue')
ax1.set_xlabel('Month')
ax1.set_ylabel('Collection Rate (%)')
ax1.set_title('Collection Rate Trend (Full Period)')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Last 12 months with decline highlights
colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in df_fin_last12['mom_change'].fillna(0)]
ax2.bar(range(len(df_fin_last12)), df_fin_last12['mom_change'], color=colors, alpha=0.8, edgecolor='white')
ax2.axhline(0, color='black', linewidth=0.5)

# Annotate values
for i, (idx, row) in enumerate(df_fin_last12.iterrows()):
    if pd.notna(row['mom_change']):
        ax2.annotate(f'{row["mom_change"]:+.1f}%', (i, row['mom_change']), 
                    ha='center', va='bottom' if row['mom_change']>0 else 'top', fontsize=8)

ax2.set_xticks(range(len(df_fin_last12)))
ax2.set_xticklabels([d.strftime('%Y-%m') for d in df_fin_last12['dashboard_month']], rotation=45, ha='right')
ax2.set_xlabel('Month')
ax2.set_ylabel('Month-over-Month Change (pp)')
ax2.set_title('Collection Rate MoM Change (Last 12 Months)')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/collection_rate_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved collection_rate_trend.png")

# 5. Cashflow forecast visualization
df_cf = db.frame(db.query("""
  SELECT forecast_month, forecasted_net_cash_flow, liquidity_status
  FROM quickbooks__cashflow_forecast
  ORDER BY forecast_month
"""))
df_cf['forecast_month'] = pd.to_datetime(df_cf['forecast_month'])

fig, ax = plt.subplots(figsize=(10, 6))

# Color by liquidity status
status_colors = {'Stable': '#2ecc71', 'At Risk': '#f39c12', 'Critical': '#e74c3c'}
bar_colors = [status_colors.get(s, '#95a5a6') for s in df_cf['liquidity_status']]

bars = ax.bar(df_cf['forecast_month'], df_cf['forecasted_net_cash_flow'], 
              color=bar_colors, edgecolor='white', width=20, alpha=0.85)

# Trend line
ax.plot(df_cf['forecast_month'], df_cf['forecasted_net_cash_flow'], 
        color='darkred', linewidth=2, marker='o', markersize=8, zorder=5)

# Annotate values
for i, row in df_cf.iterrows():
    ax.annotate(f'${row["forecasted_net_cash_flow"]:,.0f}', 
                (row['forecast_month'], row['forecasted_net_cash_flow']),
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                xytext=(0, 8), textcoords='offset points')

# Add liquidity status labels
for i, row in df_cf.iterrows():
    ax.annotate(row['liquidity_status'], 
                (row['forecast_month'], row['forecasted_net_cash_flow']/2),
                ha='center', va='center', fontsize=9, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=bar_colors[i], alpha=0.7))

ax.set_xlabel('Forecast Month')
ax.set_ylabel('Forecasted Net Cash Flow ($)')
ax.set_title('Cashflow Forecast with Liquidity Risk (Next 6 Months)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/work/cashflow_forecast.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved cashflow_forecast.png")

# 6. Profitability tier comparison
df_profit_tier = db.frame(db.query("""
  SELECT 
    CASE WHEN c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
    p.profitability_tier,
    COUNT(*) AS n_invoices,
    ROUND(SUM(p.gross_profit),2) AS total_gp
  FROM quickbooks__profitability_analysis p
  INNER JOIN quickbooks__customer_analytics c ON p.customer_id = c.customer_id
  GROUP BY risk_group, p.profitability_tier
  ORDER BY risk_group, p.profitability_tier
"""))

fig, ax = plt.subplots(figsize=(12, 6))

# Pivot for grouped bar chart
pivot = df_profit_tier.pivot_table(index='profitability_tier', columns='risk_group', values='n_invoices', fill_value=0)
pivot.plot(kind='bar', ax=ax, color=['crimson', 'steelblue'], alpha=0.8, edgecolor='white')
ax.set_xlabel('Profitability Tier')
ax.set_ylabel('Number of Invoices')
ax.set_title('Invoice Distribution by Profitability Tier: High-Risk vs Normal Customers')
ax.legend(title='Customer Group')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/profitability_tier_dist.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved profitability_tier_dist.png")

# 7. Risk score tier breakdown
risk_tiers = db.frame(db.query("""
  SELECT 
    CASE 
      WHEN risk_score < 40 THEN 'Low (30-40)'
      WHEN risk_score < 50 THEN 'Medium (40-50)'
      WHEN risk_score < 60 THEN 'High (50-60)'
      ELSE 'Critical (60+)'
    END AS risk_tier,
    COUNT(*) AS n_customers,
    ROUND(SUM(outstanding_balance),2) AS total_outstanding,
    ROUND(AVG(risk_score),2) AS avg_risk_score
  FROM (
    SELECT customer_id, outstanding_balance,
      (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
    FROM quickbooks__customer_analytics
    WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
  )
  GROUP BY risk_tier
  ORDER BY MIN(risk_score)
"""))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

tier_colors = ['#f1c40f', '#e67e22', '#e74c3c', '#8e44ad']

ax1.bar(risk_tiers['risk_tier'], risk_tiers['n_customers'], 
        color=tier_colors, edgecolor='white', alpha=0.85)
for i, row in risk_tiers.iterrows():
    ax1.annotate(f'{row["n_customers"]}', (i, row['n_customers']), 
                ha='center', va='bottom', fontweight='bold')
ax1.set_xlabel('Risk Tier')
ax1.set_ylabel('Number of Customers')
ax1.set_title('High-Risk Customers by Risk Tier')
ax1.grid(axis='y', alpha=0.3)

ax2.bar(risk_tiers['risk_tier'], risk_tiers['total_outstanding']/1e6, 
        color=tier_colors, edgecolor='white', alpha=0.85)
for i, row in risk_tiers.iterrows():
    ax2.annotate(f'${row["total_outstanding"]/1e6:.2f}M', (i, row['total_outstanding']/1e6), 
                ha='center', va='bottom', fontweight='bold')
ax2.set_xlabel('Risk Tier')
ax2.set_ylabel('Total Outstanding Balance ($M)')
ax2.set_title('Outstanding Balance by Risk Tier')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/risk_tier_breakdown.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved risk_tier_breakdown.png")

print("\nAll visualizations saved successfully.")