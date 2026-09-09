import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load persons data
persons_df = db.frame(db.query("""
  SELECT person_id, timezone, 
         count_received_email, count_opened_email, count_clicked_email,
         email_open_rate, 
         active_retention_rate_week, active_retention_rate_month,
         active_days, active_weeks, active_months,
         days_span, weeks_span, months_span,
         has_7day_retention, has_30day_retention,
         count_placed_order, count_ordered_product,
         sum_revenue_placed_order, sum_revenue_ordered_product,
         first_event_on, last_event_on
  FROM klaviyo__persons
"""))

print(f"Person records: {len(persons_df)}")
print(f"Columns: {list(persons_df.columns)}")
print(f"Timezones: {persons_df['timezone'].value_counts().to_dict()}")

# ========== Retention by timezone ==========
tz_stats = persons_df.groupby('timezone').agg(
    n=('person_id', 'count'),
    avg_ret_week=('active_retention_rate_week', 'mean'),
    avg_ret_month=('active_retention_rate_month', 'mean'),
    avg_open_rate=('email_open_rate', 'mean'),
    avg_received=('count_received_email', 'mean'),
    avg_opened=('count_opened_email', 'mean'),
    avg_orders=('count_placed_order', 'mean')
).round(4)
print("\n=== Retention by Timezone ===")
print(tz_stats)

# ANOVA for retention by timezone
tz_groups_week = [g['active_retention_rate_week'].values for _, g in persons_df.groupby('timezone')]
f_tz, p_tz = stats.f_oneway(*tz_groups_week)
print(f"\nANOVA: Retention(week) ~ Timezone: F={f_tz:.4f}, p={p_tz:.6f}")

tz_groups_month = [g['active_retention_rate_month'].values for _, g in persons_df.groupby('timezone')]
f_tz_m, p_tz_m = stats.f_oneway(*tz_groups_month)
print(f"ANOVA: Retention(month) ~ Timezone: F={f_tz_m:.4f}, p={p_tz_m:.6f}")

# ========== Retention by email volume ==========
persons_df['email_vol_group'] = pd.qcut(persons_df['count_received_email'], 
                                         q=3, labels=['Low', 'Medium', 'High'])
vol_stats = persons_df.groupby('email_vol_group', observed=True).agg(
    n=('person_id', 'count'),
    avg_ret_week=('active_retention_rate_week', 'mean'),
    avg_ret_month=('active_retention_rate_month', 'mean'),
    avg_open_rate=('email_open_rate', 'mean'),
    avg_received=('count_received_email', 'mean'),
    avg_orders=('count_placed_order', 'mean')
).round(4)
print("\n=== Retention by Email Volume Group ===")
print(vol_stats)

# ========== Retention by open rate ==========
persons_df['open_rate_group'] = pd.qcut(persons_df['email_open_rate'], 
                                         q=3, labels=['Low', 'Medium', 'High'])
or_stats = persons_df.groupby('open_rate_group', observed=True).agg(
    n=('person_id', 'count'),
    avg_ret_week=('active_retention_rate_week', 'mean'),
    avg_ret_month=('active_retention_rate_month', 'mean'),
    avg_open_rate=('email_open_rate', 'mean'),
    avg_received=('count_received_email', 'mean'),
    avg_orders=('count_placed_order', 'mean')
).round(4)
print("\n=== Retention by Open Rate Group ===")
print(or_stats)

# ========== Correlation analysis ==========
print("\n=== Correlation with Retention (Week) ===")
corr_week = persons_df[['active_retention_rate_week', 'count_received_email', 
                        'count_opened_email', 'email_open_rate',
                        'count_placed_order', 'active_days', 'days_span']].corr()
print(corr_week['active_retention_rate_week'].round(4))

print("\n=== Correlation with Retention (Month) ===")
corr_month = persons_df[['active_retention_rate_month', 'count_received_email', 
                         'count_opened_email', 'email_open_rate',
                         'count_placed_order', 'active_days', 'days_span']].corr()
print(corr_month['active_retention_rate_month'].round(4))

# ========== VISUALIZATION: Retention by timezone ==========
plt.figure(figsize=(10, 6))
tz_order = persons_df.groupby('timezone')['active_retention_rate_week'].mean().sort_values(ascending=False).index
sns.boxplot(x='timezone', y='active_retention_rate_week', data=persons_df, order=tz_order)
plt.title('Weekly Active Retention Rate by Timezone', fontsize=14)
plt.xlabel('Timezone', fontsize=12)
plt.ylabel('Active Retention Rate (Week)', fontsize=12)
plt.tight_layout()
plt.savefig('/work/boxplot_retention_by_tz.png', dpi=150)
plt.close()

# ========== VISUALIZATION: Retention vs email volume ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.scatterplot(x='count_received_email', y='active_retention_rate_week', 
                hue='timezone', data=persons_df, alpha=0.5, ax=axes[0])
axes[0].set_title('Weekly Retention vs Emails Received', fontsize=12)
axes[0].set_xlabel('Emails Received')
axes[0].set_ylabel('Retention Rate (Week)')

sns.scatterplot(x='email_open_rate', y='active_retention_rate_week', 
                hue='timezone', data=persons_df, alpha=0.5, ax=axes[1])
axes[1].set_title('Weekly Retention vs Email Open Rate', fontsize=12)
axes[1].set_xlabel('Email Open Rate')
axes[1].set_ylabel('Retention Rate (Week)')
plt.tight_layout()
plt.savefig('/work/scatter_retention_engagement.png', dpi=150)
plt.close()

# ========== Kendall/Spearman rank correlations ==========
print("\n=== Spearman Rank Correlations ===")
from scipy.stats import spearmanr
for col in ['count_received_email', 'count_opened_email', 'email_open_rate', 
            'count_placed_order', 'active_days', 'days_span']:
    r, p = spearmanr(persons_df[col], persons_df['active_retention_rate_week'])
    print(f"  {col}: r={r:.4f}, p={p:.6f}")

# ========== Summary statistics ==========
print("\n=== Overall Person Summary ===")
print(persons_df[['active_retention_rate_week', 'active_retention_rate_month',
                  'email_open_rate', 'count_received_email', 'count_placed_order']].describe().round(4))

print("\n=== PERSON ANALYSIS COMPLETE ===")