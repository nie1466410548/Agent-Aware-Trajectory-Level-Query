import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
    total_count_unique_people, count_received_email, is_archived, variation_id
  FROM klaviyo__campaigns
"""))

# De-noise using count_received_email IQR-like bounds (2%-98%)
q_low = camp_df['count_received_email'].quantile(0.02)
q_high = camp_df['count_received_email'].quantile(0.98)
clean_df = camp_df[(camp_df['count_received_email'] >= q_low) & 
                   (camp_df['count_received_email'] <= q_high)].copy()
clean_df['gmv_per_person'] = clean_df['gmv_net'] / clean_df['total_count_unique_people']
clean_df['order_rate'] = clean_df['gmv_net'] / clean_df['total_count_unique_people']

print(f"Clean dataset: {len(clean_df)} records")

# ============ Regression: Open Rate ~ Audience size (control) ============
print("\n=== OLS Regression: Open Rate ~ Audience Size (per subject group) ===")
for sg in ['discount', 'new_product', 'storytelling']:
    sub = clean_df[clean_df['subject_group'] == sg]
    slope, intercept, r, p, se = stats.linregress(sub['total_count_unique_people'], sub['email_open_rate'])
    print(f"  {sg:12s}: slope={slope:.7f}, intercept={intercept:.4f}, r={r:.4f}, p={p:.4f}")

# ============ ANOVA: by archived ============
arch_groups = [g['email_open_rate'].values for _, g in clean_df.groupby('is_archived')]
if len(arch_groups) == 2:
    f_arch, p_arch = stats.f_oneway(*arch_groups)
    print(f"\n=== ANOVA: Open Rate ~ is_archived ===")
    print(f"F={f_arch:.4f}, p={p_arch:.4f}")

# ============ ANOVA: by variation ============
var_groups = [g['email_open_rate'].values for _, g in clean_df.groupby('variation_id')]
f_var, p_var = stats.f_oneway(*var_groups)
print(f"\n=== ANOVA: Open Rate ~ variation_id ===")
print(f"F={f_var:.4f}, p={p_var:.4f}")

# ============ Detailed: archived breakdown ============
print("\n=== Archived breakdown (Open Rate by timing × subject) ===")
arch_table = clean_df.groupby(['is_archived', 'timing', 'subject_group']).agg(
    avg_open=('email_open_rate', 'mean'), n=('email_open_rate', 'count')).reset_index()
pivot_arch = arch_table.pivot_table(values='avg_open', index=['is_archived', 'timing'],
                                     columns='subject_group', aggfunc='mean')
print(pivot_arch.round(4))

# ============ Detailed: variation breakdown ============
print("\n=== Variation breakdown (Open Rate by timing × subject) ===")
var_table = clean_df.groupby(['variation_id', 'timing', 'subject_group']).agg(
    avg_open=('email_open_rate', 'mean'), n=('email_open_rate', 'count')).reset_index()
pivot_var = var_table.pivot_table(values='avg_open', index=['variation_id', 'timing'],
                                   columns='subject_group', aggfunc='mean')
print(pivot_var.round(4))

# ============ Variation summary ============
print("\n=== Variation summary ===")
print(clean_df.groupby('variation_id').agg(
    n=('email_open_rate', 'count'),
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv_pp=('gmv_per_person', 'mean')).round(4))

print("\n=== Archived summary ===")
print(clean_df.groupby('is_archived').agg(
    n=('email_open_rate', 'count'),
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv_pp=('gmv_per_person', 'mean')).round(4))

# ============ De-noising assessment ============
print("\n=== De-noising assessment ===")
print(f"Removed {len(camp_df) - len(clean_df)} outlier records at 2%-98% bounds")
removed = camp_df[(camp_df['count_received_email'] < q_low) | (camp_df['count_received_email'] > q_high)]
print(f"Removed records breakdown by timing:\n{removed['timing'].value_counts()}")
print(f"Removed records breakdown by subject:\n{removed['subject_group'].value_counts()}")

# ============ English-labeled subject bar chart ============
fig, ax = plt.subplots(figsize=(9, 6))
subj_stats = clean_df.groupby('subject_group').agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    n=('email_open_rate', 'count')
)
labels = ['Discount', 'New Product', 'Storytelling']
x = np.arange(3)
width = 0.35
ax.bar(x - width/2, subj_stats['avg_open'].values, width, label='Open Rate', color='#2E86AB', alpha=0.9)
ax.bar(x + width/2, subj_stats['avg_ctor'].values, width, label='Click-to-Open Rate', color='#A23B72', alpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel('Rate', fontsize=12)
ax.set_title('Campaign Performance by Subject Keyword Group', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
for i, v in enumerate(subj_stats['avg_open'].values):
    ax.text(i - width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10, color='#2E86AB')
for i, v in enumerate(subj_stats['avg_ctor'].values):
    ax.text(i + width/2, v + 0.005, f'{v:.3f}', ha='center', fontsize=10, color='#A23B72')
plt.tight_layout()
plt.savefig('/work/bar_subject_english.png', dpi=150)
plt.close()

# ============ Timing × subject table with orders/GMV ============
print("\n=== Timing × Subject: Key Metrics ===")
interact = clean_df.groupby(['timing', 'subject_group']).agg(
    avg_open=('email_open_rate', 'mean'),
    avg_ctor=('email_click_to_open_rate', 'mean'),
    avg_gmv_pp=('gmv_per_person', 'mean'),
    avg_audience=('total_count_unique_people', 'mean'),
    n=('email_open_rate', 'count')).round(4)
print(interact)

print("\n=== FINAL ANALYSIS COMPLETE ===")