import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Create a comprehensive dashboard figure
fig, axes = plt.subplots(3, 3, figsize=(18, 16))

# 1. Segment-level metrics
seg_data = {'segment': ['new_contract', 'renewal', 'expansion', 'churn_watch'],
            'avg_resp': [25.88, 26.09, 26.18, 25.90],
            'bot_pct': [33.08, 32.32, 32.83, 34.15],
            'weekly_ret': [65.97, 70.98, 73.98, 59.98],
            'monthly_ret': [55.48, 64.31, 69.48, 45.32],
            'conv_rate': [3.03, 2.87, 2.88, 1.91]}
df = pd.DataFrame(seg_data)
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']

# Panel 1: Response Delay
axes[0,0].bar(df['segment'], df['avg_resp'], color=colors, alpha=0.85)
axes[0,0].set_title('Avg Response Delay (minutes)', fontsize=12, fontweight='bold')
axes[0,0].set_ylabel('Minutes')
for i, v in enumerate(df['avg_resp']):
    axes[0,0].text(i, v+0.15, f'{v:.2f}', ha='center', fontsize=9)

# Panel 2: Bot Ratio
axes[0,1].bar(df['segment'], df['bot_pct'], color=colors, alpha=0.85)
axes[0,1].set_title('Bot Response Ratio (%)', fontsize=12, fontweight='bold')
axes[0,1].set_ylabel('%')
for i, v in enumerate(df['bot_pct']):
    axes[0,1].text(i, v+0.3, f'{v:.2f}%', ha='center', fontsize=9)

# Panel 3: Retention
x = np.arange(len(df))
w = 0.35
axes[0,2].bar(x - w/2, df['weekly_ret'], w, label='Weekly', color='steelblue', alpha=0.85)
axes[0,2].bar(x + w/2, df['monthly_ret'], w, label='Monthly', color='lightcoral', alpha=0.85)
axes[0,2].set_xticks(x)
axes[0,2].set_xticklabels(df['segment'])
axes[0,2].set_title('Retention Rate (%)', fontsize=12, fontweight='bold')
axes[0,2].set_ylabel('%')
axes[0,2].legend(fontsize=9)
for i in range(len(df)):
    axes[0,2].text(i - w/2, df['weekly_ret'].iloc[i] + 0.8, f'{df["weekly_ret"].iloc[i]:.1f}', ha='center', fontsize=8)
    axes[0,2].text(i + w/2, df['monthly_ret'].iloc[i] + 0.8, f'{df["monthly_ret"].iloc[i]:.1f}', ha='center', fontsize=8)

# Panel 4: Conversion Rate
axes[1,0].bar(df['segment'], df['conv_rate'], color=colors, alpha=0.85)
axes[1,0].set_title('Conversation-to-Feature-Usage Conversion (%)', fontsize=12, fontweight='bold')
axes[1,0].set_ylabel('%')
for i, v in enumerate(df['conv_rate']):
    axes[1,0].text(i, v+0.05, f'{v:.2f}%', ha='center', fontsize=9)

# Panel 5: ARR Bucket Retention
arr_ret_data = {'arr': ['<30k', '30k_65k', '65k_110k', '110k_200k', '200k_plus'],
                'weekly': [73.57, 71.71, 67.70, 63.25, 59.95],
                'monthly': [69.07, 65.24, 58.52, 50.85, 45.28]}
arr_df = pd.DataFrame(arr_ret_data)
x = np.arange(len(arr_df))
w = 0.35
axes[1,1].bar(x - w/2, arr_df['weekly'], w, label='Weekly', color='steelblue', alpha=0.85)
axes[1,1].bar(x + w/2, arr_df['monthly'], w, label='Monthly', color='lightcoral', alpha=0.85)
axes[1,1].set_xticks(x)
axes[1,1].set_xticklabels(arr_df['arr'], rotation=30, fontsize=8)
axes[1,1].set_title('Retention by ARR Bucket (%)', fontsize=12, fontweight='bold')
axes[1,1].set_ylabel('%')
axes[1,1].legend(fontsize=9)

# Panel 6: Seat Bucket Retention
seat_ret_data = {'seat': ['under_60', '60_129', '130_259', '260_419', '420_plus'],
                 'weekly': [73.84, 72.46, 68.52, 63.91, 59.90],
                 'monthly': [69.35, 66.81, 59.96, 52.05, 45.08]}
seat_df = pd.DataFrame(seat_ret_data)
x = np.arange(len(seat_df))
w = 0.35
axes[1,2].bar(x - w/2, seat_df['weekly'], w, label='Weekly', color='steelblue', alpha=0.85)
axes[1,2].bar(x + w/2, seat_df['monthly'], w, label='Monthly', color='lightcoral', alpha=0.85)
axes[1,2].set_xticks(x)
axes[1,2].set_xticklabels(seat_df['seat'], rotation=30, fontsize=8)
axes[1,2].set_title('Retention by Seat Bucket (%)', fontsize=12, fontweight='bold')
axes[1,2].set_ylabel('%')
axes[1,2].legend(fontsize=9)

# Panel 7: SLA by Segment
sla_data = {'segment': ['new_contract', 'renewal', 'expansion', 'churn_watch'],
            'breached': [75.2, 75.6, 74.9, 74.2],
            'met': [2.9, 3.1, 2.3, 2.8],
            'warning': [21.8, 21.3, 22.9, 23.1]}
sla_df = pd.DataFrame(sla_data)
x = np.arange(len(sla_df))
w = 0.25
axes[2,0].bar(x - w, sla_df['breached'], w, label='Breached', color='#E74C3C', alpha=0.85)
axes[2,0].bar(x, sla_df['met'], w, label='Met', color='#2ECC71', alpha=0.85)
axes[2,0].bar(x + w, sla_df['warning'], w, label='Warning', color='#F39C12', alpha=0.85)
axes[2,0].set_xticks(x)
axes[2,0].set_xticklabels(sla_df['segment'])
axes[2,0].set_title('SLA Status by Segment (%)', fontsize=12, fontweight='bold')
axes[2,0].set_ylabel('%')
axes[2,0].legend(fontsize=8)

# Panel 8: Monthly Trends
monthly_data = {'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'convs': [970, 1196, 1275, 1239, 1271, 621],
                'bot_pct': [33.30, 32.94, 33.33, 32.93, 33.20, 32.69]}
mon_df = pd.DataFrame(monthly_data)
axes[2,1].plot(mon_df['month'], mon_df['convs'], marker='o', color='steelblue', linewidth=2)
axes[2,1].set_title('Monthly Conversation Volume', fontsize=12, fontweight='bold')
axes[2,1].set_ylabel('Conversations')
axes[2,1].grid(alpha=0.3)
ax2 = axes[2,1].twinx()
ax2.plot(mon_df['month'], mon_df['bot_pct'], marker='s', color='darkorange', linewidth=2, linestyle='--')
ax2.set_ylabel('Bot %', color='darkorange')

# Panel 9: Bot vs Human Response Time
axes[2,2].bar(['Bot', 'Human'], [23.0, 27.49], color=['#3498DB', '#E74C3C'], alpha=0.85)
axes[2,2].set_title('Avg Response Time (min): Bot vs Human', fontsize=12, fontweight='bold')
axes[2,2].set_ylabel('Minutes')
for i, v in enumerate([23.0, 27.49]):
    axes[2,2].text(i, v+0.3, f'{v:.2f}', ha='center', fontsize=10)

fig.suptitle('Intercom Customer Engagement Metrics Dashboard\n(Jan-Jun 2024, Outlier-Filtered)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/work/comprehensive_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("Dashboard saved.")