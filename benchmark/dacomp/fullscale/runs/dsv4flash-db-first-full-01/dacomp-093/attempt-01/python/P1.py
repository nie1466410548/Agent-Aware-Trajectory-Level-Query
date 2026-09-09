import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import os

# Load campaign data
camp_df = db.frame(db.query("""
  SELECT
    campaign_id, campaign_name, SUBJECT, is_archived, variation_id,
    SENT_AT, total_count_unique_people, count_received_email,
    count_opened_email, count_clicked_email, email_open_rate,
    email_click_to_open_rate, count_placed_order, gmv_net,
    product_view_to_order_rate_campaign, active_days, total_placed_orders,
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    strftime('%Y-%m', SENT_AT) AS sent_month
  FROM klaviyo__campaigns
"""))

print(f"Campaign records: {len(camp_df)}")
print(f"Timing categories: {camp_df['timing'].value_counts().to_dict()}")
print(f"Subject groups: {camp_df['subject_group'].value_counts().to_dict()}")
print(f"Archived: {camp_df['is_archived'].value_counts().to_dict()}")

# Prepare cleaned dataset (de-noise: exclude top/bottom 2% by count_received_email)
quantiles = camp_df['count_received_email'].quantile([0.02, 0.98])
clean_df = camp_df[
    (camp_df['count_received_email'] >= quantiles[0.02]) &
    (camp_df['count_received_email'] <= quantiles[0.98])
].copy()
print(f"\nAfter de-noising: {len(clean_df)} records (removed {len(camp_df)-len(clean_df)})")

# ========== TWO-WAY ANOVA: open_rate ~ timing * subject_group ==========
# Since we have unbalanced groups, use Type II/III ANOVA
from statsmodels.api import stats as sm_stats

formula = 'email_open_rate ~ C(timing) * C(subject_group)'
model = ols(formula, data=clean_df).fit()
anova_results = anova_lm(model, typ=2)
print("\n=== Two-Way ANOVA: Open Rate ~ Timing * Subject ===")
print(anova_results)

# ========== TWO-WAY ANOVA: CTOR ~ timing * subject_group ==========
formula2 = 'email_click_to_open_rate ~ C(timing) * C(subject_group)'
model2 = ols(formula2, data=clean_df).fit()
anova_results2 = anova_lm(model2, typ=2)
print("\n=== Two-Way ANOVA: CTOR ~ Timing * Subject ===")
print(anova_results2)

# ========== VISUALIZATION 1: Heatmap of open rates ==========
plt.figure(figsize=(12, 8))
pivot_open = clean_df.pivot_table(
    values='email_open_rate', 
    index='timing', 
    columns='subject_group', 
    aggfunc='mean'
)
# Reorder index for better display
timing_order = ['weekday_morning', 'weekday_afternoon', 'weekday_evening',
                'weekend_morning', 'weekend_evening', 'pre_holiday_afternoon']
pivot_open = pivot_open.reindex(timing_order)
sns.heatmap(pivot_open, annot=True, fmt='.3f', cmap='RdYlGn', 
            linewidths=0.5, vmin=0.2, vmax=0.42)
plt.title('Average Email Open Rate by Timing × Subject Group', fontsize=14)
plt.tight_layout()
plt.savefig('/work/heatmap_open_rate.png', dpi=150)
plt.close()

# ========== VISUALIZATION 2: Heatmap of CTOR ==========
plt.figure(figsize=(12, 8))
pivot_ctor = clean_df.pivot_table(
    values='email_click_to_open_rate', 
    index='timing', 
    columns='subject_group', 
    aggfunc='mean'
)
pivot_ctor = pivot_ctor.reindex(timing_order)
sns.heatmap(pivot_ctor, annot=True, fmt='.3f', cmap='RdYlGn',
            linewidths=0.5, vmin=0.1, vmax=0.17)
plt.title('Average Click-to-Open Rate by Timing × Subject Group', fontsize=14)
plt.tight_layout()
plt.savefig('/work/heatmap_ctor.png', dpi=150)
plt.close()

# ========== VISUALIZATION 3: Bar chart by timing ==========
plt.figure(figsize=(14, 6))
timing_stats = clean_df.groupby('timing').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv_per_person=('gmv_net', lambda x: x.sum() / clean_df.loc[x.index, 'total_count_unique_people'].sum()),
    n=('email_open_rate', 'count')
).reindex(timing_order)
print("\n=== Timing Performance ===")
print(timing_stats)

x = np.arange(len(timing_order))
width = 0.35
fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.bar(x - width/2, timing_stats['avg_open'].values, width, label='Open Rate', color='steelblue', alpha=0.8)
ax1.set_ylabel('Open Rate', fontsize=12)
ax1.set_ylim(0, 0.5)
for i, v in enumerate(timing_stats['avg_open'].values):
    ax1.text(i - width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=9)
ax2 = ax1.twinx()
ax2.bar(x + width/2, timing_stats['avg_ctor'].values, width, label='Click-to-Open Rate', color='coral', alpha=0.8)
ax2.set_ylabel('Click-to-Open Rate', fontsize=12)
ax2.set_ylim(0, 0.25)
for i, v in enumerate(timing_stats['avg_ctor'].values):
    ax2.text(i + width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=9)
ax1.set_xticks(x)
ax1.set_xticklabels([t.replace('_', '\n') for t in timing_order], fontsize=10)
fig.suptitle('Email Performance by Planned Send Timing', fontsize=14)
fig.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/work/bar_timing_performance.png', dpi=150)
plt.close()

# ========== VISUALIZATION 4: Bar chart by subject ==========
plt.figure(figsize=(10, 6))
subj_stats = clean_df.groupby('subject_group').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    n=('email_open_rate', 'count')
)
print("\n=== Subject Group Performance ===")
print(subj_stats)

x = np.arange(len(subj_stats.index))
width = 0.35
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(x - width/2, subj_stats['avg_open'].values, width, label='Open Rate', color='steelblue', alpha=0.8)
ax1.set_ylabel('Open Rate', fontsize=12)
ax1.set_ylim(0, 0.5)
for i, v in enumerate(subj_stats['avg_open'].values):
    ax1.text(i - width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10)
ax2 = ax1.twinx()
ax2.bar(x + width/2, subj_stats['avg_ctor'].values, width, label='Click-to-Open Rate', color='coral', alpha=0.8)
ax2.set_ylabel('Click-to-Open Rate', fontsize=12)
ax2.set_ylim(0, 0.25)
for i, v in enumerate(subj_stats['avg_ctor'].values):
    ax2.text(i + width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(subj_stats.index, fontsize=11)
fig.suptitle('Email Performance by Subject Keyword Group', fontsize=14)
fig.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/work/bar_subject_performance.png', dpi=150)
plt.close()

# ========== VISUALIZATION 5: Audience size control ==========
plt.figure(figsize=(10, 6))
scatter = plt.scatter(clean_df['total_count_unique_people'], clean_df['email_open_rate'],
                      c=clean_df['subject_group'].map({'discount': 'red', 'new_product': 'blue', 'storytelling': 'green'}),
                      alpha=0.6, s=40)
plt.xlabel('Audience Size (total_count_unique_people)', fontsize=12)
plt.ylabel('Email Open Rate', fontsize=12)
plt.title('Open Rate vs Audience Size (colored by subject group)', fontsize=14)
# Add regression line
from numpy.polynomial.polynomial import polyfit
b, m = polyfit(clean_df['total_count_unique_people'], clean_df['email_open_rate'], 1)
plt.plot(clean_df['total_count_unique_people'], 
         b + m * clean_df['total_count_unique_people'], 
         'k--', alpha=0.5, label=f'Slope={m:.6f}')
plt.legend()
plt.tight_layout()
plt.savefig('/work/scatter_audience_vs_open.png', dpi=150)
plt.close()

# Correlation matrix
print("\n=== Correlation Matrix (selected metrics) ===")
corr_cols = ['email_open_rate', 'email_click_to_open_rate', 'total_count_unique_people',
             'count_received_email', 'gmv_net', 'product_view_to_order_rate_campaign',
             'total_placed_orders', 'active_days']
corr_df = clean_df[corr_cols].corr()
print(corr_df.round(4))

print("\n=== Analysis Complete ===")
print(f"Figures saved to /work/")