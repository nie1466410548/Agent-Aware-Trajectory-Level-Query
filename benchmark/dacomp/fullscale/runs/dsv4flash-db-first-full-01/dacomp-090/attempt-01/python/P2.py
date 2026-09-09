import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 1. Load high-risk customer data with risk scores
df_risk = db.frame(db.query("""
  SELECT customer_id, outstanding_balance, payment_rate_percentage, credit_score, 
         business_stability_score, overdue_count_12m, avg_payment_days_12m,
         (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
"""))

# 2. Load collection rate data
df_collect = db.frame(db.query("""
  SELECT dashboard_month, collection_rate_percentage, outstanding_receivables, overdue_amount
  FROM quickbooks__financial_dashboard
  ORDER BY dashboard_month
"""))
df_collect['dashboard_month'] = pd.to_datetime(df_collect['dashboard_month'])

# 3. Load cashflow forecast
df_cf = db.frame(db.query("""
  SELECT forecast_month, forecasted_net_cash_flow, liquidity_status
  FROM quickbooks__cashflow_forecast
  ORDER BY forecast_month
"""))
df_cf['forecast_month'] = pd.to_datetime(df_cf['forecast_month'])

# === Risk Warning Model ===

# Current collection rate (latest month)
current_collection_rate = df_collect['collection_rate_percentage'].iloc[-1]
print(f"Current collection rate: {current_collection_rate:.2f}%")

# Total outstanding balance of high-risk customers
total_outstanding = df_risk['outstanding_balance'].sum()
print(f"Total outstanding balance (high-risk): ${total_outstanding:,.2f}")

# Risk-weighted expected loss (risk score as probability of non-collection)
df_risk['expected_loss_risk'] = df_risk['outstanding_balance'] * (df_risk['risk_score'] / 100.0)
total_expected_loss = df_risk['expected_loss_risk'].sum()
print(f"Risk-weighted expected loss: ${total_expected_loss:,.2f}")
print(f"Expected recovery rate: {(1 - total_expected_loss/total_outstanding)*100:.2f}%")

# Scenario Analysis
print("\n===== SCENARIO ANALYSIS =====")

# Scenario 1: Base (current recovery rate)
scenario1_recovery = total_outstanding * (current_collection_rate / 100)
scenario1_loss = total_outstanding - scenario1_recovery
print(f"Scenario 1 (Base - current collection rate {current_collection_rate:.2f}%):")
print(f"  Expected recovery: ${scenario1_recovery:,.2f}")
print(f"  Expected loss: ${scenario1_loss:,.2f}")

# Scenario 2: Risk-weighted (using composite risk score)
scenario2_recovery = total_outstanding - total_expected_loss
print(f"Scenario 2 (Risk-weighted model):")
print(f"  Expected recovery: ${scenario2_recovery:,.2f}")
print(f"  Expected loss: ${total_expected_loss:,.2f}")

# Scenario 3: Pessimistic (if collection rate continues declining)
# Monthly decline rate in last 3 months (most recent streak)
last3 = df_collect.tail(3)
monthly_decline = last3['collection_rate_percentage'].diff().mean()
print(f"Average monthly decline (last 3 months): {monthly_decline:.2f}pp")

# Projected collection rate after 6 months
projected_rate = max(0, current_collection_rate + monthly_decline * 6)
print(f"Projected collection rate after 6 months: {projected_rate:.2f}%")
scenario3_recovery = total_outstanding * (projected_rate / 100)
scenario3_loss = total_outstanding - scenario3_recovery
print(f"Scenario 3 (Pessimistic - declining trend):")
print(f"  Projected recovery: ${scenario3_recovery:,.2f}")
print(f"  Projected loss: ${scenario3_loss:,.2f}")

# Scenario 4: Worst-case (risk score + declining trend)
# Use risk-weighted probability but with declining collection rate
effective_rate = projected_rate / 100
scenario4_loss = total_expected_loss * (1 + abs(monthly_decline/current_collection_rate) * 3)
print(f"Scenario 4 (Worst-case combined):")
print(f"  Estimated loss: ${scenario4_loss:,.2f}")

# === Cashflow impact assessment ===
print("\n===== CASHFLOW IMPACT =====")
total_cf_6m = df_cf['forecasted_net_cash_flow'].sum()
print(f"Total forecasted net cash flow (6 months): ${total_cf_6m:,.2f}")
print(f"High-risk outstanding as % of 6-month cashflow: {total_outstanding/total_cf_6m*100:.1f}%")
print(f"Expected loss as % of 6-month cashflow: {total_expected_loss/total_cf_6m*100:.1f}%")

# === Visualization: Scenario Comparison ===
fig, ax = plt.subplots(figsize=(12, 6))

scenarios = ['Base\n(Current Rate)', 'Risk-Weighted\n(Composite Score)', 'Pessimistic\n(Declining Trend)', 'Worst-Case\n(Combined)']
recovery_values = [scenario1_recovery/1e6, scenario2_recovery/1e6, scenario3_recovery/1e6, (total_outstanding - scenario4_loss)/1e6]
loss_values = [scenario1_loss/1e6, total_expected_loss/1e6, scenario3_loss/1e6, scenario4_loss/1e6]

x = np.arange(len(scenarios))
width = 0.35

bars1 = ax.bar(x - width/2, recovery_values, width, label='Expected Recovery', color='#2ecc71', alpha=0.85, edgecolor='white')
bars2 = ax.bar(x + width/2, loss_values, width, label='Expected Loss', color='#e74c3c', alpha=0.85, edgecolor='white')

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'${height:.2f}M', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'${height:.2f}M', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.set_ylabel('Amount ($ Millions)')
ax.set_title('Risk Warning Model: Projected Loss Scenarios (Next 6 Months)')
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}M'))

plt.tight_layout()
plt.savefig('/work/risk_warning_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved risk_warning_model.png")

# === Outstanding by risk tier for strategies ===
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
    ROUND(AVG(risk_score),2) AS avg_risk_score,
    ROUND(AVG(avg_payment_days_12m),1) AS avg_pay_days,
    ROUND(AVG(overdue_count_12m),2) AS avg_overdue
  FROM (
    SELECT customer_id, outstanding_balance, avg_payment_days_12m, overdue_count_12m,
      (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
    FROM quickbooks__customer_analytics
    WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
  )
  GROUP BY risk_tier
  ORDER BY MIN(risk_score)
"""))
print("\n===== RISK TIER BREAKDOWN =====")
print(risk_tiers.to_string(index=False))

print("\n===== MODEL COMPLETE =====")