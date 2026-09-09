import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
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

# Prepare cleaned dataset (de-noise: exclude top/bottom 2% by count_received_email)
q_low = camp_df['count_received_email'].quantile(0.02)
q_high = camp_df['count_received_email'].quantile(0.98)
clean_df = camp_df[
    (camp_df['count_received_email'] >= q_low) &
    (camp_df['count_received_email'] <= q_high)
].copy()
print(f"\nAfter de-noising: {len(clean_df)} records (removed {len(camp_df)-len(clean_df)})")

# ========== ONE-WAY ANOVA for timing effect on open rate ==========
timing_groups = [g['email_open_rate'].values for _, g in clean_df.groupby('timing')]
f_stat, p_val = stats.f_oneway(*timing_groups)
print(f"\n=== One-Way ANOVA: Open Rate ~ Timing ===")
print(f"F-statistic: {f_stat:.4f}, p-value: {p_val:.6f}")

# ========== ONE-WAY ANOVA for subject effect on open rate ==========
subj_groups = [g['email_open_rate'].values for _, g in clean_df.groupby('subject_group')]
f_stat2, p_val2 = stats.f_oneway(*subj_groups)
print(f"\n=== One-Way ANOVA: Open Rate ~ Subject Group ===")
print(f"F-statistic: {f_stat2:.4f}, p-value: {p_val2:.6f}")

# ========== ONE-WAY ANOVA for timing effect on CTOR ==========
timing_ctor = [g['email_click_to_open_rate'].values for _, g in clean_df.groupby('timing')]
f_stat3, p_val3 = stats.f_oneway(*timing_ctor)
print(f"\n=== One-Way ANOVA: CTOR ~ Timing ===")
print(f"F-statistic: {f_stat3:.4f}, p-value: {p_val3:.6f}")

# ========== ONE-WAY ANOVA for subject effect on CTOR ==========
subj_ctor = [g['email_click_to_open_rate'].values for _, g in clean_df.groupby('subject_group')]
f_stat4, p_val4 = stats.f_oneway(*subj_ctor)
print(f"\n=== One-Way ANOVA: CTOR ~ Subject Group ===")
print(f"F-statistic: {f_stat4:.4f}, p-value: {p_val4:.6f}")

# ========== Two-way interaction via group means ==========
print("\n=== Interaction Means (Timing × Subject) ===")
interaction = clean_df.groupby(['timing', 'subject_group'])['email_open_rate'].agg(['mean', 'std', 'count'])
print(interaction.round(4))

# ========== VISUALIZATION 1: Heatmap of open rates ==========
plt.figure(figsize=(12, 8))
pivot_open = clean_df.pivot_table(
    values='email_open_rate', 
    index='timing', 
    columns='subject_group', 
    aggfunc='mean'
)
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
timing_stats = clean_df.groupby('timing').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv=('gmv_net', 'mean'),
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

# ========== VISUALIZATION 5: Audience size scatter ==========
plt.figure(figsize=(10, 6))
colors = {'discount': 'red', 'new_product': 'blue', 'storytelling': 'green'}
for sg in ['discount', 'new_product', 'storytelling']:
    subset = clean_df[clean_df['subject_group'] == sg]
    plt.scatter(subset['total_count_unique_people'], subset['email_open_rate'],
                c=colors[sg], alpha=0.6, s=40, label=sg)
plt.xlabel('Audience Size (total_count_unique_people)', fontsize=12)
plt.ylabel('Email Open Rate', fontsize=12)
plt.title('Open Rate vs Audience Size (colored by subject group)', fontsize=14)
# Regression line
from numpy.polynomial.polynomial import polyfit
b, m = polyfit(clean_df['total_count_unique_people'], clean_df['email_open_rate'], 1)
plt.plot(clean_df['total_count_unique_people'], 
         b + m * clean_df['total_count_unique_people'], 
         'k--', alpha=0.5, label=f'Overall trend (slope={m:.6f})')
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

# ========== VISUALIZATION 6: Archived vs non-archived ==========
arch_stats = clean_df.groupby(['is_archived', 'timing', 'subject_group']).agg(
    avg_open=('email_open_rate', 'mean'),
    n=('email_open_rate', 'count')
).reset_index()
print("\n=== Archived vs Non-Archived Interaction ===")
print(arch_stats.pivot_table(values='avg_open', index=['is_archived', 'timing'], 
                             columns='subject_group', aggfunc='mean').round(4))

# ========== VISUALIZATION 7: Variation ID analysis ==========
var_stats = clean_df.groupby(['variation_id', 'timing', 'subject_group']).agg(
    avg_open=('email_open_rate', 'mean'),
    n=('email_open_rate', 'count')
).reset_index()
print("\n=== Variation ID Interaction ===")
print(var_stats.pivot_table(values='avg_open', index=['variation_id', 'timing'], 
                           columns='subject_group', aggfunc='mean').round(4))

# ========== VISUALIZATION 8: GMV per person by timing and subject ==========
clean_df['gmv_per_person'] = clean_df['gmv_net'] / clean_df['total_count_unique_people']
gmv_pivot = clean_df.pivot_table(values='gmv_per_person', index='timing', 
                                  columns='subject_group', aggfunc='mean').reindex(timing_order)
print("\n=== GMV per Person by Timing × Subject ===")
print(gmv_pivot.round(4))

plt.figure(figsize=(12, 8))
sns.heatmap(gmv_pivot, annot=True, fmt='.4f', cmap='YlOrRd', linewidths=0.5)
plt.title('Average GMV per Person by Timing × Subject Group', fontsize=14)
plt.tight_layout()
plt.savefig('/work/heatmap_gmv_per_person.png', dpi=150)
plt.close()

print("\n=== ANALYSIS COMPLETE ===")
print("Figures saved to /work/")