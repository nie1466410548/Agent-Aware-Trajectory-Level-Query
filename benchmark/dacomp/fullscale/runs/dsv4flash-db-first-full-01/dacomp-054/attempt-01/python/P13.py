import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/cohort_data.csv')

# Create platform pattern column
def platform_label(row):
    m = row['in_marketo']; s = row['in_stripe']; z = row['in_zendesk']
    if m and s and z: return 'All 3 Platforms'
    if m and s and not z: return 'Marketo+Stripe'
    if m and not s and z: return 'Marketo+Zendesk'
    if not m and s and z: return 'Stripe+Zendesk'
    if m and not s and not z: return 'Marketo Only'
    if not m and s and not z: return 'Stripe Only'
    if not m and not s and z: return 'Zendesk Only'
    return 'None'

df['platform_pattern'] = df.apply(platform_label, axis=1)

# ANOVA: effect of platform pattern on customer_health_score
groups = [g.values for _, g in df.groupby('platform_pattern')['customer_health_score']]
f_stat, p_val = stats.f_oneway(*groups)
print(f"ANOVA Platform Pattern: F={f_stat:.4f}, p={p_val:.6f}")

# Engagement velocity ANOVA
groups2 = [g.values for _, g in df.groupby('engagement_velocity')['customer_health_score']]
f2, p2 = stats.f_oneway(*groups2)
print(f"ANOVA Engagement Velocity: F={f2:.4f}, p={p2:.6f}")

# Activity risk level ANOVA 
groups3 = [g.values for _, g in df.groupby('activity_risk_level')['customer_health_score']]
f3, p3 = stats.f_oneway(*groups3)
print(f"ANOVA Risk Level: F={f3:.4f}, p={p3:.6f}")

# Correlations
corr_vars = ['customer_health_score', 'composite_engagement_score', 'funnel_ltv', 
             'cross_platform_consistency', 'activity_efficiency', 'days_since_last_activity',
             'churn_probability', 'investment_priority_score', 'estimated_monthly_activities']
corr_matrix = df[corr_vars].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# Visualization 1: Platform pattern vs Health Score
plt.figure(figsize=(12, 6))
order = ['All 3 Platforms', 'Marketo+Stripe', 'Marketo+Zendesk', 'Stripe+Zendesk',
         'Marketo Only', 'Stripe Only', 'Zendesk Only', 'None']
sns.boxplot(data=df, x='platform_pattern', y='customer_health_score', order=order)
plt.title('Customer Health Score by Multi-Platform Engagement Pattern (Cohort)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/work/fig1_platform_health.png')
plt.close()

# Visualization 2: Risk Level x Engagement Velocity heatmap
pivot = df.pivot_table(values='customer_health_score', index='activity_risk_level', 
                       columns='engagement_velocity', aggfunc='mean')
plt.figure(figsize=(10, 7))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=70)
plt.title('Avg Health Score: Risk Level × Engagement Velocity', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig2_risk_velocity_heatmap.png')
plt.close()

# Visualization 3: LTV by tier
plt.figure(figsize=(10, 6))
tier_order = ['Basic', 'Bronze', 'Silver', 'Gold', 'Platinum']
sns.boxplot(data=df, x='customer_tier', y='funnel_ltv', order=tier_order)
plt.title('Estimated Customer LTV by Tier (Cohort)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig3_ltv_by_tier.png')
plt.close()

# Visualization 4: Risk category distribution
plt.figure(figsize=(8, 8))
risk_counts = df['risk_category'].value_counts()
plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Risk Category Distribution (Cohort)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig4_risk_category.png')
plt.close()

# Visualization 5: Platform pattern distribution
plt.figure(figsize=(10, 6))
plat_counts = df['platform_pattern'].value_counts()
sns.barplot(x=plat_counts.index, y=plat_counts.values)
plt.xticks(rotation=45)
plt.title('Multi-Platform Engagement Pattern Distribution (Cohort)', fontsize=14)
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('/work/fig5_platform_dist.png')
plt.close()

print("All figures saved successfully")

# Summary stats for the report
print("\n--- Summary Statistics ---")
print(f"Cohort Size: {len(df)}")
print(f"Average RFM scores: Recency={df['composite_engagement_score'].mean():.2f} (composite proxy)")
print(f"Average LTV: ${df['funnel_ltv'].mean():.2f}")
print(f"Average Health Score: {df['customer_health_score'].mean():.2f}")
print(f"Zendesk Active: {df['zendesk_active'].sum()}/{len(df)} = {df['zendesk_active'].mean()*100:.2f}%")
print(f"Platform completers (all 3): {(df['in_marketo']*df['in_stripe']*df['in_zendesk']).sum()}")

# Cross-tab: platform pattern vs health score
print("\n--- Platform Pattern Summary ---")
print(df.groupby('platform_pattern').agg({
    'customer_health_score': ['mean', 'std', 'count'],
    'funnel_ltv': 'mean'
}).round(2))

# Risk-velocity matrix
print("\n--- Risk × Velocity Health Score Matrix ---")
print(pivot.round(2))