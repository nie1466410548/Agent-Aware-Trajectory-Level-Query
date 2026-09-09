import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

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
low_health = df[df['health_score'] < 50].copy()

risk_matrix = pd.crosstab(low_health['industry_normalized'], low_health['account_size_segment'], margins=True, margins_name='Total')
print("=== RISK WARNING MATRIX: Count (Health < 50) ===")
print(risk_matrix)

total_matrix = pd.crosstab(df['industry_normalized'], df['account_size_segment'], margins=True, margins_name='Total')
risk_pct = (risk_matrix / total_matrix * 100).round(1)
print("\nRisk Percentage Matrix (% of segment):")
print(risk_pct)

# Heatmap (drop Total)
risk_pct_hm = risk_pct.drop('Total', axis=0).drop('Total', axis=1).astype(float)
plt.figure(figsize=(11, 5))
sns.heatmap(risk_pct_hm, annot=True, cmap='YlOrRd', fmt='.1f', linewidths=1,
            cbar_kws={'label': '% of Segment with Health < 50'})
plt.title('Customer Risk Warning Matrix\n% of Accounts with Health Score < 50 by Industry and Size', fontsize=13, fontweight='bold')
plt.ylabel('Industry')
plt.xlabel('Account Size Segment')
plt.tight_layout()
plt.savefig('/work/risk_warning_matrix.png', dpi=150)
plt.close()

# ===== ANALYSIS 2: Revenue Contribution Prediction Model =====
df['account_age_months'] = df['account_age_days'] / 30.44
df['monthly_won_rate'] = df['total_won_amount'] / df['account_age_months'].clip(lower=1)
df['health_factor'] = df['health_score'] / 100.0
df['renewal_base'] = df['health_factor'] * df['monthly_won_rate'] * 6
df['pipeline_upside'] = df['health_factor'] * (df['win_rate_percentage'] / 100.0) * df['current_pipeline_amount']
df['predicted_6mo_revenue'] = df['renewal_base'] + df['pipeline_upside']

print("\n\n=== REVENUE CONTRIBUTION PREDICTION MODEL ===")
print(f"Predicted 6-month revenue: min=${df['predicted_6mo_revenue'].min():,.0f} max=${df['predicted_6mo_revenue'].max():,.0f}")
print(f"Mean=${df['predicted_6mo_revenue'].mean():,.0f} Median=${df['predicted_6mo_revenue'].median():,.0f}")
print(f"Total predicted 6-month contribution: ${df['predicted_6mo_revenue'].sum():,.0f}")

df['revenue_tier'] = pd.qcut(df['predicted_6mo_revenue'], q=5, labels=['Tier 5 (Lowest)', 'Tier 4', 'Tier 3', 'Tier 2', 'Tier 1 (Highest)'])
print("\nRevenue Tier Distribution:")
print(df['revenue_tier'].value_counts().sort_index())

print("\nAvg Predicted Revenue by Health Category:")
print(df.groupby('health_category')['predicted_6mo_revenue'].agg(['count','mean','median','sum']).round(0))

# Tier summary
print("\nTier summary stats:")
tier_summary = df.groupby('revenue_tier', observed=False).agg(
    n=('account_id','count'),
    mean_pred=('predicted_6mo_revenue','mean'),
    sum_pred=('predicted_6mo_revenue','sum'),
    mean_health=('health_score','mean'),
    mean_rev=('annual_revenue','mean')
).round(0)
print(tier_summary)

# Visualization 2
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(df['health_score'], df['predicted_6mo_revenue']/1e6, alpha=0.25, s=5, c='steelblue')
axes[0].set_xlabel('Health Score')
axes[0].set_ylabel('Predicted 6-Month Revenue ($M)')
axes[0].set_title('Health Score vs Predicted 6-Month Revenue')
axes[0].grid(True, alpha=0.3)

tier_order = ['Tier 5 (Lowest)', 'Tier 4', 'Tier 3', 'Tier 2', 'Tier 1 (Highest)']
df_box = df.copy()
df_box['revenue_tier'] = pd.Categorical(df_box['revenue_tier'], categories=tier_order, ordered=True)
df_box.boxplot(column='predicted_6mo_revenue', by='revenue_tier', ax=axes[1], grid=False)
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
print("\nCustomer Count by Health Category and Size Segment:")
print(pd.crosstab(df['health_category'], df['account_size_segment']))

print("\nKey Metrics by Health Category:")
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
    print(f"  Avg Win Rate: {sub['win_rate_percentage'].mean():.1f}%")

# Health score distribution
plt.figure(figsize=(10, 5))
plt.hist(df['health_score'], bins=40, color='steelblue', edgecolor='white', alpha=0.7)
plt.axvline(50, color='red', linestyle='--', linewidth=2, label='Low-Health Threshold (<50)')
plt.axvline(80, color='green', linestyle='--', linewidth=2, label='High-Health Threshold (80+)')
plt.xlabel('Health Score')
plt.ylabel('Number of Accounts')
plt.title('Distribution of Calculated Customer Health Scores (n=10,000)')
plt.legend()
plt.tight_layout()
plt.savefig('/work/health_score_distribution.png', dpi=150)
plt.close()

# Save full scored dataset for reference
df.to_csv('/work/customer_health_scores.csv', index=False)
print("\nSaved /work/customer_health_scores.csv with", len(df), "rows")
print("All figures saved.")