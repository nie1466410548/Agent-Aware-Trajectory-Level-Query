import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the analysis dataset from the SQL result
# Read the full rows from the archived result
import json
rows = []
with open('/results/S20.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)
print("Dataset columns:", df.columns.tolist())
print("\nFull dataset:")
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

print("\n=== Cross-tab: Mean open_rate by theme × day_part ===")
print(df.groupby(['theme','day_part'])['open_rate'].mean())

print("\n=== Cross-tab: Mean click_rate by day_part × time_half ===")
print(df.groupby(['day_part','time_half'])['click_rate'].mean())

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

# 1. Open rate by theme and day_part
for i, (metric, title) in enumerate(zip(
    ['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month',
     'net_revenue_touch','open_rate'],
    ['Open Rate','Click Rate','Active Retention (Week)','Active Retention (Month)',
     'Net Revenue','Open Rate']
)):
    if i < 5:
        ax = axes[i//3, i%3]
        # Theme × Day_part interaction
        pivot = df.pivot_table(values=metric, index='theme', columns='day_part', aggfunc='mean')
        pivot.plot(kind='bar', ax=ax, alpha=0.7)
        ax.set_title(f'{title} by Theme × Day Part', fontsize=11)
        ax.set_ylabel(title)
        ax.set_xlabel('Subject Theme')
        ax.legend(title='Day Part')
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    else:
        ax = axes[1, 2]  # placeholder for the 6th plot

# Adjust layout
plt.tight_layout()
plt.savefig('/work/interaction_analysis.png', dpi=150, bbox_inches='tight')
print("\nSaved interaction_analysis.png")

# Create a detailed heatmap-like plot
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4))
fig2.suptitle('Metric Means by Theme × Day Type × Time Half', fontsize=13, fontweight='bold')

for idx, metric in enumerate(['open_rate','click_rate','active_retention_rate_week']):
    ax = axes2[idx]
    pivot = df.pivot_table(values=metric, index='theme', 
                           columns=['day_part','time_half'], aggfunc='mean')
    # Flatten columns
    pivot.columns = [f'{c[0]}_{c[1]}' for c in pivot.columns]
    pivot.T.plot(kind='bar', ax=ax, alpha=0.7)
    ax.set_title(metric.replace('_',' ').title())
    ax.set_ylabel('Mean Value')
    ax.legend(title='Theme')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

plt.tight_layout()
plt.savefig('/work/metrics_by_theme_and_timing.png', dpi=150, bbox_inches='tight')
print("Saved metrics_by_theme_and_timing.png")

# Create a table visualization of the raw data
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

# Two-way interaction analysis using OLS (if enough data, but with N=4 it's just illustrative)
print("\n=== Two-Way Interaction Descriptive Statistics ===")
# Create interaction groups
df['interaction_group'] = df['theme'] + ' × ' + df['day_part'] + ' × ' + df['time_half']
print(df.groupby('interaction_group')[['open_rate','click_rate','active_retention_rate_week','active_retention_rate_month']].describe())

# Save the processed data for the report
df.to_csv('/work/analysis_dataset.csv', index=False)
print("Saved analysis_dataset.csv")