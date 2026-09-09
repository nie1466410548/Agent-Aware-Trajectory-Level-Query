import pandas as pd
import numpy as np

# Compute health scores and full dataset
df = db.frame(db.query("""
  WITH scores AS (
    SELECT 
      account_id,
      account_name,
      industry_normalized,
      account_size_segment,
      number_of_employees,
      annual_revenue,
      total_won_amount,
      current_pipeline_amount,
      win_rate_percentage,
      account_age_days,
      total_contacts,
      contacts_with_email,
      days_since_last_activity,
      total_activities_30d,
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

print("Health score distribution:")
print(df['health_score'].describe())
print("\nHealth score percentiles:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    print(f"  p{p}: {df['health_score'].quantile(p/100):.1f}")

print("\n\nHealth score categories:")
print(pd.cut(df['health_score'], bins=[0, 50, 80, 100], labels=['Low (<50)', 'Medium (50-80)', 'High (80+)']).value_counts())

print("\n\nBy industry:")
print(df.groupby('industry_normalized')['health_score'].describe())

print("\n\nBy account size:")
print(df.groupby('account_size_segment')['health_score'].describe())

# Count low health accounts
low = df[df['health_score'] < 50]
print(f"\n\nAccounts with health < 50: {len(low)} out of {len(df)} ({len(low)/len(df)*100:.1f}%)")

# Low health by industry and size
print("\n\nLow health (<50) by industry x size:")
ct = pd.crosstab(low['industry_normalized'], low['account_size_segment'])
print(ct)
print("\nPercentages of total per industry-size:")
total_ct = pd.crosstab(df['industry_normalized'], df['account_size_segment'])
print((ct / total_ct * 100).round(1))