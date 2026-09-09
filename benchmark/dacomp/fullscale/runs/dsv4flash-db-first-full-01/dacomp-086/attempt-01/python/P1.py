import pandas as pd
import numpy as np

# Load all the data we need
df = db.frame(db.query("SELECT account_id, days_since_last_activity, total_activities_30d, total_contacts, contacts_with_email, annual_revenue, total_won_amount, account_size_segment, number_of_employees, industry_normalized, current_pipeline_amount, customer_health_score, churn_risk_level, account_name, account_type FROM salesforce__customer_360_view"))

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nBasic stats:")
print(df[['days_since_last_activity', 'total_activities_30d', 'total_contacts', 'contacts_with_email', 'annual_revenue', 'total_won_amount', 'number_of_employees', 'current_pipeline_amount']].describe())

print("\n\naccount_size_segment distribution:")
print(df['account_size_segment'].value_counts())

print("\n\nindustry_normalized distribution:")
print(df['industry_normalized'].value_counts())

print("\n\ncontact_email_ratio stats:")
ratio = df['contacts_with_email'] / df['total_contacts'].replace(0, 1)
print(ratio.describe())

print("\n\nExisting customer_health_score stats:")
print(df['customer_health_score'].describe())
print(df['customer_health_score'].value_counts().sort_index().head(20))
print("...")
print(df['customer_health_score'].value_counts().sort_index().tail(20))