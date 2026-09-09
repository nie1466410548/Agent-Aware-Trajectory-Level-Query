import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Full dataset with all scores
df = db.frame(db.query("""
  WITH scores AS (
    SELECT 
      account_id, account_name, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, current_pipeline_amount, win_rate_percentage, account_age_days,
      total_contacts, contacts_with_email, days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *,
    ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores
"""))

df['health_category'] = pd.cut(df['health_score'], bins=[0, 50, 80, 100], labels=['Low (<50)', 'Medium (50-80)', 'High (80+)'])

# ===== ANALYSIS 1: Risk Warning Matrix =====

# Low health accounts (health < 50)
low_health = df[df['health_score'] < 50].copy()

print("=== RISK WARNING MATRIX ===")
print(f"Total accounts with Health < 50: {len(low_health)} ({len(low_health)/len(df)*100:.1f}%)")

# Risk matrix: industry x size
risk_matrix = pd.crosstab(
    low_health['industry_normalized'], 
    low_health['account_size_segment'],
    margins=True, margins_name='Total'
)
print("\nRisk Count Matrix (Health < 50):")
print(risk_matrix)

# Percentage of total in each segment
total_matrix = pd.crosstab(df['industry_normalized'], df['account_size_segment'], margins=True, margins_name='Total')
risk_pct = (risk_matrix / total_matrix * 100).round(1)
print("\nRisk Percentage Matrix (% of segment):")
print(risk_pct)

# Common characteristics of low health accounts
print("\n\nCommon Characteristics of Low Health (<50) Accounts:")
print(low_health[['activity_score', 'contact_score', 'value_score', 'scale_score', 
                   'days_since_last_activity', 'total_activities_30d', 'annual_revenue',
                   'total_won_amount']].describe())

# Compare low vs medium vs high
print("\n\nComparison by Health Category:")
summary = df.groupby('health_category')[['activity_score', 'contact_score', 'value_score', 'scale_score',
                                           'days_since_last_activity', 'total_activities_30d',
                                           'annual_revenue', 'total_won_amount']].describe()
print(summary)

# ===== VISUALIZATION 1: Risk Heatmap =====
plt.figure(figsize=(12, 6))
# Prepare data for heatmap
risk_pct_clean = risk_pct.drop('Total', level=0, axis=0).drop('Total', level=1, axis=1) if 'Total' in risk_pct.index and 'Total' in risk_pct.columns else risk_pct
risk_pct_clean = risk_pct.drop('Total', axis=0).drop('Total', axis=1)
sns.heatmap(risk_pct_clean.astype(float), annot=True, cmap='YlOrRd', fmt='.1f', 
            linewidths=1, cbar_kws={'label': '% of Segment with Health < 50'})
plt.title('Customer Risk Warning Matrix: % of Accounts with Health Score < 50\nby Industry and Size Segment', fontsize=14, fontweight='bold')
plt.ylabel('Industry')
plt.xlabel('Account Size Segment')
plt.tight_layout()
plt.savefig('/work/risk_warning_matrix.png', dpi=150)
plt.close()

# ===== ANALYSIS 2: Revenue Contribution Prediction Model =====

# Model: predicted_6mo_revenue = health_factor * (historical_won_rate * 6) + health_factor * win_rate * pipeline
# Where historical monthly won rate = total_won_amount / (account_age_days / 30.44)
# health_factor = health_score / 100 (as a risk adjustment multiplier)

df['account_age_months'] = df['account_age_days'] / 30.44
df['monthly_won_rate'] = df['total_won_amount'] / df['account_age_months'].clip(lower=1)
df['health_factor'] = df['health_score'] / 100.0

# Renewal base: 6-month retained revenue from historical won rate, adjusted by health (healthier = more likely to retain)
df['renewal_base'] = df['health_factor'] * df['monthly_won_rate'] * 6

# Pipeline upside: pipeline * win_rate * health_factor (healthier = more likely to convert)
df['pipeline_upside'] = df['health_factor'] * (df['win_rate_percentage'] / 100.0) * df['current_pipeline_amount']

df['predicted_6mo_revenue'] = df['renewal_base'] + df['pipeline_upside']

print("\n\n=== REVENUE CONTRIBUTION PREDICTION MODEL ===")
print(f"Predicted 6-month revenue range: ${df['predicted_6mo_revenue'].min():,.0f} - ${df['predicted_6mo_revenue'].max():,.0f}")
print(f"Mean predicted: ${df['predicted_6mo_revenue'].mean():,.0f}")
print(f"Median predicted: ${df['predicted_6mo_revenue'].median():,.0f}")

# Tier customers by predicted contribution
# Define tiers based on predicted contribution
df['revenue_tier'] = pd.qcut(df['predicted_6mo_revenue'], q=5, labels=['Tier 5 (Lowest)', 'Tier 4', 'Tier 3', 'Tier 2', 'Tier 1 (Highest)'])

print("\nRevenue Tier Distribution:")
print(df['revenue_tier'].value_counts().sort_index())

# By health score range
print("\n\nAvg Predicted Revenue by Health Category:")
print(df.groupby('health_category')['predicted_6mo_revenue'].describe())

# ===== VISUALIZATION 2: Revenue by Health and Tier =====
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter: health vs predicted revenue
axes[0].scatter(df['health_score'], df['predicted_6mo_revenue']/1e6, alpha=0.3, s=5, c='steelblue')
axes[0].set_xlabel('Health Score')
axes[0].set_ylabel('Predicted 6-Month Revenue ($M)')
axes[0].set_title('Health Score vs Predicted Revenue Contribution')
axes[0].grid(True, alpha=0.3)

# Boxplot: revenue by tier
tier_order = ['Tier 5 (Lowest)', 'Tier 4', 'Tier 3', 'Tier 2', 'Tier 1 (Highest)']
df_box = df.copy()
df_box['revenue_tier'] = pd.Categorical(df_box['revenue_tier'], categories=tier_order, ordered=True)
bp = df_box.boxplot(column='predicted_6mo_revenue', by='revenue_tier', ax=axes[1], grid=False)
axes[1].set_title('Predicted 6-Month Revenue by Tier')
axes[1].set_xlabel('Revenue Tier')
axes[1].set_ylabel('Predicted Revenue ($)')
axes[1].tick_params(axis='x', rotation=45)
plt.suptitle('')
plt.tight_layout()
plt.savefig('/work/revenue_prediction.png', dpi=150)
plt.close()

# ===== ANALYSIS 3: Differentiated Strategies =====

print("\n\n=== DIFFERENTIATED CUSTOMER SUCCESS STRATEGIES ===")

# Summary by health category and size
print("\n\nCustomer Count by Health Category and Size Segment:")
strategy_matrix = pd.crosstab(df['health_category'], df['account_size_segment'])
print(strategy_matrix)

# Avg metrics by health category and size
print("\n\nAvg Health Score by Health Category and Size:")
print(df.groupby(['health_category', 'account_size_segment'])['health_score'].agg(['mean', 'count']).round(1))

# Key metrics for strategy formulation
print("\n\nKey Metrics for Strategy Formulation:")
for cat in ['Low (<50)', 'Medium (50-80)', 'High (80+)']:
    sub = df[df['health_category'] == cat]
    print(f"\n--- {cat} (n={len(sub)}) ---")
    print(f"  Avg Days Since Activity: {sub['days_since_last_activity'].mean():.1f}")
    print(f"  Avg Activities (30d): {sub['total_activities_30d'].mean():.1f}")
    print(f"  Avg Contact Email Ratio: {(sub['contacts_with_email']/sub['total_contacts']).mean():.3f}")
    print(f"  Avg Annual Revenue: ${sub['annual_revenue'].mean():,.0f}")
    print(f"  Avg Total Won: ${sub['total_won_amount'].mean():,.0f}")
    print(f"  Avg Pipeline: ${sub['current_pipeline_amount'].mean():,.0f}")
    print(f"  Avg Predicted 6mo Revenue: ${sub['predicted_6mo_revenue'].mean():,.0f}")

# Health score distribution histogram
plt.figure(figsize=(10, 5))
plt.hist(df['health_score'], bins=40, color='steelblue', edgecolor='white', alpha=0.7)
plt.axvline(50, color='red', linestyle='--', label='Low Risk Threshold')
plt.axvline(80, color='green', linestyle='--', label='High Health Threshold')
plt.xlabel('Health Score')
plt.ylabel('Number of Accounts')
plt.title('Distribution of Calculated Customer Health Scores')
plt.legend()
plt.tight_layout()
plt.savefig('/work/health_score_distribution.png', dpi=150)
plt.close()

print("\n\nAnalysis complete. All visualizations saved.")