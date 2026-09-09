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
groups = [g for _, g in df.groupby('platform_pattern')['customer_health_score']]
f_stat, p_val = stats.f_oneway(*groups)
print(f"ANOVA: F={f_stat:.4f}, p={p_val:.6f}")

# Tukey HSD for pairwise comparisons
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(df['customer_health_score'], df['platform_pattern'], alpha=0.05)
print("\nTukey HSD:")
print(tukey)

# Also check engagement_velocity and activity_risk_level on health score
f2, p2 = stats.f_oneway(*[g for _, g in df.groupby('engagement_velocity')['customer_health_score']])
print(f"\nEngagement Velocity ANOVA: F={f2:.4f}, p={p2:.6f}")

f3, p3 = stats.f_oneway(*[g for _, g in df.groupby('activity_risk_level')['customer_health_score']])
print(f"Activity Risk Level ANOVA: F={f3:.4f}, p={p3:.6f}")

# Correlations
corr_vars = ['customer_health_score', 'composite_engagement_score', 'funnel_ltv', 
             'cross_platform_consistency', 'activity_efficiency', 'days_since_last_activity',
             'churn_probability', 'investment_priority_score', 'estimated_monthly_activities']
corr_matrix = df[corr_vars].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# Visualization 1: Platform pattern vs Health Score
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='platform_pattern', y='customer_health_score', 
            order=['All 3 Platforms', 'Marketo+Stripe', 'Marketo+Zendesk', 'Stripe+Zendesk',
                   'Marketo Only', 'Stripe Only', 'Zendesk Only', 'None'])
plt.title('Customer Health Score by Multi-Platform Engagement Pattern (Cohort)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/work/fig1_platform_health.png')
plt.close()

# Visualization 2: Risk Level x Engagement Velocity heatmap of avg health score
risk_order = ['Very Low', 'Low', 'Medium', 'High', 'Critical', 'High Activity Risk']
vel_order = ['Accelerating', 'Stable', 'Declining', 'Volatile', 'Stagnant']
pivot = df.pivot_table(values='customer_health_score', index='activity_risk_level', 
                       columns='engagement_velocity', aggfunc='mean')
plt.figure(figsize=(10, 7))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=70)
plt.title('Avg Health Score: Risk Level × Engagement Velocity', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig2_risk_velocity_heatmap.png')
plt.close()

# Visualization 3: LTV distribution by tier for cohort
plt.figure(figsize=(10, 6))
tier_order = ['Basic', 'Bronze', 'Silver', 'Gold', 'Platinum']
sns.boxplot(data=df, x='customer_tier', y='funnel_ltv', order=tier_order)
plt.title('Estimated Customer LTV by Tier (Cohort)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig3_ltv_by_tier.png')
plt.close()

# Visualization 4: Engagement velocity distribution pie
plt.figure(figsize=(8, 8))
vel_counts = df['engagement_velocity'].value_counts()
plt.pie(vel_counts.values, labels=vel_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Engagement Velocity Distribution (Cohort)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig4_velocity_pie.png')
plt.close()

print("All figures saved")