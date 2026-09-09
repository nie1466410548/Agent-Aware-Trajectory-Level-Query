import pandas as pd
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Column names from the S20 query result (in order)
columns = ['person_id', 'campaign_id', 'campaign_name', 'campaign_subject_line', 'send_at',
           'open_rate', 'click_rate', 'count_received_email', 'count_opened_email', 'count_clicked_email',
           'net_revenue_touch', 'active_retention_rate_week', 'active_retention_rate_month',
           'person_email_open_rate', 'dow', 'hour', 'day_part', 'time_half', 'theme',
           'holiday', 'hol_diff', 'holiday_window']

# Load rows
rows = []
with open('/results/S20.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=columns)
print("Full dataset:")
print(df[['person_id','campaign_id','campaign_name','campaign_subject_line','send_at',
          'open_rate','click_rate','day_part','time_half','theme','holiday_window',
          'active_retention_rate_week','active_retention_rate_month']].to_string(index=False))

# Summary statistics
print("\n=== Summary Statistics ===")
metrics = ['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month']
print(df[metrics].describe())

# Cross-tabulations
print("\n=== Cross-tab: Mean open_rate by day_part × time_half ===")
print(df.groupby(['day_part','time_half'])['open_rate'].mean())

print("\n=== Cross-tab: Mean click_rate by day_part × time_half ===")
print(df.groupby(['day_part','time_half'])['click_rate'].mean())

print("\n=== Cross-tab: Mean open_rate by theme × day_part ===")
print(df.groupby(['theme','day_part'])['open_rate'].mean())

print("\n=== Cross-tab: Mean click_rate by theme × day_part ===")
print(df.groupby(['theme','day_part'])['click_rate'].mean())

print("\n=== Cross-tab: Mean retention_week by theme × day_part ===")
print(df.groupby(['theme','day_part'])['active_retention_rate_week'].mean())

print("\n=== Cross-tab: Mean retention_month by theme × day_part ===")
print(df.groupby(['theme','day_part'])['active_retention_rate_month'].mean())

# Create interaction visualization
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Interactive Impact of Timing Windows and Subject Themes on Email Metrics', 
             fontsize=14, fontweight='bold', y=1.02)

metric_list = ['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month',
               'net_revenue_touch']
title_list = ['Open Rate','Click Rate','Active Retention (Week)','Active Retention (Month)',
              'Net Revenue']

for i, (metric, title) in enumerate(zip(metric_list, title_list)):
    ax = axes[i//3, i%3]
    pivot = df.pivot_table(values=metric, index='theme', columns='day_part', aggfunc='mean')
    pivot.plot(kind='bar', ax=ax, alpha=0.7)
    ax.set_title(f'{title} by Theme × Day Part', fontsize=11)
    ax.set_ylabel(title)
    ax.set_xlabel('Subject Theme')
    ax.legend(title='Day Part')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

# 6th plot: Theme × time_half for open rate
ax = axes[1, 2]
pivot2 = df.pivot_table(values='open_rate', index='theme', columns='time_half', aggfunc='mean')
pivot2.plot(kind='bar', ax=ax, alpha=0.7)
ax.set_title('Open Rate by Theme × Time Half', fontsize=11)
ax.set_ylabel('Open Rate')
ax.set_xlabel('Subject Theme')
ax.legend(title='Time Half')
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

plt.tight_layout()
plt.savefig('/work/interaction_analysis.png', dpi=150, bbox_inches='tight')
print("\nSaved interaction_analysis.png")

# Create a detailed table visualization
fig3, ax3 = plt.subplots(figsize=(16, 3))
ax3.axis('off')
table_data = df[['campaign_id','campaign_name','theme','day_part','time_half','holiday_window',
                 'open_rate','click_rate','active_retention_rate_week']].copy()
table_data['open_rate'] = table_data['open_rate'].round(3)
table_data['click_rate'] = table_data['click_rate'].round(3)
table = ax3.table(cellText=table_data.values, colLabels=table_data.columns,
                  cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)
ax3.set_title('Campaign-Person Touch Analysis Dataset', fontsize=14, fontweight='bold', pad=20)
plt.savefig('/work/analysis_dataset_table.png', dpi=150, bbox_inches='tight')
print("Saved analysis_dataset_table.png")

# Detailed interaction groups
df['interaction_group'] = df['theme'] + ' × ' + df['day_part'] + ' × ' + df['time_half']
print("\n=== Interaction Group Means ===")
print(df.groupby('interaction_group')[['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month']].mean())

# Also compute person-level stats for context
print("\n=== Person-level context (from klaviyo__persons) ===")
print("Person 01F366... (2 touches):", 
      df[df.person_id == '01F366M1ZERT4HM2Z9R2V9G7BY'][['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month','person_email_open_rate']].iloc[0].to_dict())
print("Person 59bc05... (2 touches):",
      df[df.person_id == '59bc0505-cb93-40a1-9524-437521d13454'][['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month','person_email_open_rate']].iloc[0].to_dict())

# Save the processed data
df.to_csv('/work/analysis_dataset.csv', index=False)
print("Saved analysis_dataset.csv")