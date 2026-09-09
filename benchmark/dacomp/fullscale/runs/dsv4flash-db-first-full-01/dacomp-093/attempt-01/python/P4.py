import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
camp_df = db.frame(db.query("""
  SELECT
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
    email_open_rate, email_click_to_open_rate, gmv_net,
    total_count_unique_people, is_archived, variation_id
  FROM klaviyo__campaigns
"""))

# De-noise
q_low = camp_df['email_open_rate'].quantile(0.01)
q_high = camp_df['email_open_rate'].quantile(0.99)
clean_df = camp_df[(camp_df['email_open_rate'] >= q_low) & (camp_df['email_open_rate'] <= q_high)]

# Combined figure
timing_order = ['weekday_morning', 'weekday_afternoon', 'weekday_evening',
                'weekend_morning', 'weekend_evening', 'pre_holiday_afternoon']
timing_labels = ['Weekday\nMorning', 'Weekday\nAfternoon', 'Weekday\nEvening',
                 'Weekend\nMorning', 'Weekend\nEvening', 'Pre-Holiday\nAfternoon']

fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Plot 1: Open Rate by timing and subject
pivot_open = clean_df.pivot_table(values='email_open_rate', index='timing', 
                                   columns='subject_group', aggfunc='mean').reindex(timing_order)
sns.heatmap(pivot_open, annot=True, fmt='.3f', cmap='RdYlGn', linewidths=0.5, 
            vmin=0.22, vmax=0.41, ax=axes[0])
axes[0].set_title('Email Open Rate\n(Timing × Subject Group)', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Send Timing', fontsize=11)
axes[0].set_xlabel('Subject Keyword Group', fontsize=11)

# Plot 2: CTOR by timing and subject
pivot_ctor = clean_df.pivot_table(values='email_click_to_open_rate', index='timing', 
                                   columns='subject_group', aggfunc='mean').reindex(timing_order)
sns.heatmap(pivot_ctor, annot=True, fmt='.3f', cmap='RdYlGn', linewidths=0.5,
            vmin=0.10, vmax=0.17, ax=axes[1])
axes[1].set_title('Click-to-Open Rate\n(Timing × Subject Group)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Send Timing', fontsize=11)
axes[1].set_xlabel('Subject Keyword Group', fontsize=11)

# Plot 3: GMV per person by timing and subject
clean_df['gmv_per_person'] = clean_df['gmv_net'] / clean_df['total_count_unique_people']
pivot_gmv = clean_df.pivot_table(values='gmv_per_person', index='timing', 
                                  columns='subject_group', aggfunc='mean').reindex(timing_order)
sns.heatmap(pivot_gmv, annot=True, fmt='.4f', cmap='YlOrRd', linewidths=0.5, ax=axes[2])
axes[2].set_title('GMV per Person\n(Timing × Subject Group)', fontsize=13, fontweight='bold')
axes[2].set_ylabel('Send Timing', fontsize=11)
axes[2].set_xlabel('Subject Keyword Group', fontsize=11)

plt.tight_layout()
plt.savefig('/work/combined_heatmaps.png', dpi=150)
plt.close()

# ========== Bar chart: Timing main effects ==========
fig, ax = plt.subplots(figsize=(12, 6))
timing_stats = clean_df.groupby('timing').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv=('gmv_net', 'mean'),
    n=('email_open_rate', 'count')
).reindex(timing_order)

x = np.arange(len(timing_order))
width = 0.25
ax.bar(x - width, timing_stats['avg_open'].values, width, label='Open Rate', color='#2E86AB', alpha=0.9)
ax.bar(x, timing_stats['avg_ctor'].values, width, label='Click-to-Open Rate', color='#A23B72', alpha=0.9)
ax.bar(x + width, timing_stats['avg_gmv'].values / 20000, width, label='GMV (scaled /20000)', color='#F18F01', alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels(timing_labels, fontsize=10)
ax.set_ylabel('Rate', fontsize=12)
ax.set_title('Campaign Performance by Send Timing\n(Controlling for Audience Size, De-noised)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.axhline(y=clean_df['email_open_rate'].mean(), color='#2E86AB', linestyle='--', alpha=0.3)
ax.axhline(y=clean_df['email_click_to_open_rate'].mean(), color='#A23B72', linestyle='--', alpha=0.3)

for i, v in enumerate(timing_stats['avg_open'].values):
    ax.text(i - width, v + 0.005, f'{v:.3f}', ha='center', fontsize=8, color='#2E86AB')
for i, v in enumerate(timing_stats['avg_ctor'].values):
    ax.text(i, v + 0.005, f'{v:.3f}', ha='center', fontsize=8, color='#A23B72')

plt.tight_layout()
plt.savefig('/work/bar_timing_combined.png', dpi=150)
plt.close()

# ========== Bar chart: Subject main effects ==========
fig, ax = plt.subplots(figsize=(10, 6))
subj_stats = clean_df.groupby('subject_group').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    n=('email_open_rate', 'count')
)

x = np.arange(len(subj_stats.index))
width = 0.35
ax.bar(x - width/2, subj_stats['avg_open'].values, width, label='Open Rate', color='#2E86AB', alpha=0.9)
ax.bar(x + width/2, subj_stats['avg_ctor'].values, width, label='Click-to-Open Rate', color='#A23B72', alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels(['Discount\n(限时折扣)', 'New Product\n(新品上新)', 'Storytelling\n(品牌故事)'], fontsize=11)
ax.set_ylabel('Rate', fontsize=12)
ax.set_title('Campaign Performance by Subject Keyword Group\n(De-noised)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)

for i, v in enumerate(subj_stats['avg_open'].values):
    ax.text(i - width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10, color='#2E86AB')
for i, v in enumerate(subj_stats['avg_ctor'].values):
    ax.text(i + width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10, color='#A23B72')

plt.tight_layout()
plt.savefig('/work/bar_subject_combined.png', dpi=150)
plt.close()

print("Combined figures saved successfully.")
print(f"Timing stats:\n{timing_stats}")
print(f"\nSubject stats:\n{subj_stats}")