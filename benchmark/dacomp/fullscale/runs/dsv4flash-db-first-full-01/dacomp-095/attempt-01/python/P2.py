import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 120, 'figure.facecolor': 'white'})

# ============== 1. Lifecycle Stage Comparison ==============
stages = ['Cold Start\n(2mo)', 'Growth\n(3mo)', 'Mature\n(4mo)', 'Peak\n(5mo)']
n_persons = [166, 365, 463, 198]
avg_orders = [3.24, 1.21, 1.70, 0.39]
avg_revenue = [304.7, 118.1, 189.9, 48.1]
avg_open = [60.0, 51.3, 36.9, 26.0]
avg_span = [56, 80, 111, 139]
avg_emails = [65.2, 65.8, 84.3, 90.9]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
x = np.arange(len(stages))

# Orders
ax = axes[0,0]; ax.bar(x, avg_orders, color=['#2ecc71','#3498db','#f39c12','#e74c3c'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(stages); ax.set_title('Average Orders per Person', fontweight='bold')
ax.set_ylabel('Orders'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(avg_orders): ax.text(i, v+0.08, f'{v:.2f}', ha='center', fontweight='bold')

# Revenue
ax = axes[0,1]; ax.bar(x, avg_revenue, color=['#2ecc71','#3498db','#f39c12','#e74c3c'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(stages); ax.set_title('Average Revenue ($)', fontweight='bold')
ax.set_ylabel('Revenue ($)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(avg_revenue): ax.text(i, v+3, f'${v:.0f}', ha='center', fontweight='bold')

# Open Rate
ax = axes[0,2]; ax.bar(x, avg_open, color=['#2ecc71','#3498db','#f39c12','#e74c3c'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(stages); ax.set_title('Email Open Rate (%)', fontweight='bold')
ax.set_ylabel('Open Rate (%)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(avg_open): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontweight='bold')

# Days Span
ax = axes[1,0]; ax.bar(x, avg_span, color=['#2ecc71','#3498db','#f39c12','#e74c3c'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(stages); ax.set_title('Average Days Span (Time to Peak)', fontweight='bold')
ax.set_ylabel('Days'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(avg_span): ax.text(i, v+2, f'{v:.0f}d', ha='center', fontweight='bold')

# Emails Received
ax = axes[1,1]; ax.bar(x, avg_emails, color=['#2ecc71','#3498db','#f39c12','#e74c3c'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(stages); ax.set_title('Average Emails Received', fontweight='bold')
ax.set_ylabel('Emails'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(avg_emails): ax.text(i, v+1, f'{v:.0f}', ha='center', fontweight='bold')

# Pct of population
ax = axes[1,2]; ax.pie(n_persons, labels=['Cold Start\n(14%)','Growth\n(31%)','Mature\n(39%)','Peak\n(17%)'],
                        colors=['#2ecc71','#3498db','#f39c12','#e74c3c'], autopct='%1.0f%%', startangle=90)
ax.set_title('Population Distribution', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/lifecycle_stages.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved")

# ============== 2. Speed Group Analysis ==============
speed_groups = ['Fast\n(≤60d)', 'Medium\n(61-90d)', 'Slow\n(91-120d)', 'Very Slow\n(>120d)']
n_s = [133, 331, 398, 330]
orders_s = [2.95, 1.74, 1.36, 1.02]
revenue_s = [277.0, 167.3, 151.2, 117.3]
open_s = [60.1, 54.0, 39.7, 28.2]
prr_s = [1.0, 0.967, 0.958, 0.920]
emails_s = [63.9, 64.9, 80.0, 91.1]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
x = np.arange(len(speed_groups))

# Orders
ax = axes[0,0]; ax.bar(x, orders_s, color='#3498db', width=0.6)
ax.set_xticks(x); ax.set_xticklabels(speed_groups); ax.set_title('Orders by Speed Group', fontweight='bold')
ax.set_ylabel('Avg Orders'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(orders_s): ax.text(i, v+0.06, f'{v:.2f}', ha='center', fontweight='bold')

# Revenue
ax = axes[0,1]; ax.bar(x, revenue_s, color='#3498db', width=0.6)
ax.set_xticks(x); ax.set_xticklabels(speed_groups); ax.set_title('Revenue by Speed Group', fontweight='bold')
ax.set_ylabel('Avg Revenue ($)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(revenue_s): ax.text(i, v+3, f'${v:.0f}', ha='center', fontweight='bold')

# Open Rate
ax = axes[0,2]; ax.bar(x, open_s, color='#3498db', width=0.6)
ax.set_xticks(x); ax.set_xticklabels(speed_groups); ax.set_title('Email Open Rate by Speed Group', fontweight='bold')
ax.set_ylabel('Open Rate (%)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(open_s): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontweight='bold')

# Retention Rate
ax = axes[1,0]; ax.plot(x, prr_s, 'o-', color='#e74c3c', linewidth=2.5, markersize=10)
ax.set_xticks(x); ax.set_xticklabels(speed_groups); ax.set_title('Paid Retention Rate by Speed Group', fontweight='bold')
ax.set_ylabel('Retention Rate'); ax.grid(True, alpha=0.3); ax.set_ylim(0.85, 1.02)
for i,v in enumerate(prr_s): ax.text(i, v+0.008, f'{v:.3f}', ha='center', fontweight='bold')

# Emails Received
ax = axes[1,1]; ax.bar(x, emails_s, color='#3498db', width=0.6)
ax.set_xticks(x); ax.set_xticklabels(speed_groups); ax.set_title('Emails Received by Speed Group', fontweight='bold')
ax.set_ylabel('Avg Emails'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(emails_s): ax.text(i, v+1, f'{v:.0f}', ha='center', fontweight='bold')

# Population
ax = axes[1,2]; ax.pie(n_s, labels=speed_groups, colors=['#2ecc71','#3498db','#f39c12','#e74c3c'],
                        autopct='%1.1f%%', startangle=90)
ax.set_title('Population by Speed Group', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/speed_groups.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved")

# ============== 3. Campaign Efficiency ==============
campaigns = ['VIP', 'Product\nLaunch', 'Promotion', 'Digest', 'Flash\nSale', 'Newsletter', 'Survey', 'Winback']
gmv_per_recv = [3.68, 1.74, 0.91, 0.80, 0.67, 0.48, 0.45, 0.20]
orders_per_recv = [0.0215, 0.0125, 0.0077, 0.0045, 0.0052, 0.0038, 0.0030, 0.0015]
open_rate = [52.0, 48.0, 40.9, 34.0, 27.0, 36.0, 32.0, 22.0]
ctr = [23.0, 20.0, 17.0, 13.0, 16.0, 12.0, 12.0, 7.9]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
x = np.arange(len(campaigns))

# GMV per received
ax = axes[0,0]; colors = ['#9b59b6','#3498db','#2ecc71','#f39c12','#e74c3c','#1abc9c','#e67e22','#95a5a6']
bars = ax.bar(x, gmv_per_recv, color=colors, width=0.6)
ax.set_xticks(x); ax.set_xticklabels(campaigns); ax.set_title('GMV per Email Received', fontweight='bold')
ax.set_ylabel('GMV ($) per Received'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(gmv_per_recv): ax.text(i, v+0.05, f'${v:.2f}', ha='center', fontweight='bold', fontsize=9)

# Orders per received
ax = axes[0,1]; bars = ax.bar(x, orders_per_recv, color=colors, width=0.6)
ax.set_xticks(x); ax.set_xticklabels(campaigns); ax.set_title('Orders per Email Received', fontweight='bold')
ax.set_ylabel('Orders per Received'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(orders_per_recv): ax.text(i, v+0.0003, f'{v:.4f}', ha='center', fontweight='bold', fontsize=9)

# Open rate
ax = axes[1,0]; bars = ax.bar(x, open_rate, color=colors, width=0.6)
ax.set_xticks(x); ax.set_xticklabels(campaigns); ax.set_title('Email Open Rate by Campaign Type', fontweight='bold')
ax.set_ylabel('Open Rate (%)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(open_rate): ax.text(i, v+0.5, f'{v:.0f}%', ha='center', fontweight='bold', fontsize=9)

# Click-to-Open Rate
ax = axes[1,1]; bars = ax.bar(x, ctr, color=colors, width=0.6)
ax.set_xticks(x); ax.set_xticklabels(campaigns); ax.set_title('Click-to-Open Rate by Campaign Type', fontweight='bold')
ax.set_ylabel('CTOR (%)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(ctr): ax.text(i, v+0.3, f'{v:.0f}%', ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('/work/campaign_efficiency.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved")

# ============== 4. Frequency vs Open Rate Scatter ==============
df = db.frame(db.query("SELECT count_received_email, email_open_rate, count_placed_order, days_span FROM klaviyo__persons"))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Emails vs Open Rate
ax = axes[0]
sc = ax.scatter(df['count_received_email'], df['email_open_rate'], 
                c=df['count_placed_order'], cmap='viridis', alpha=0.5, s=15)
ax.set_xlabel('Total Emails Received')
ax.set_ylabel('Email Open Rate')
ax.set_title('Email Frequency vs Open Rate (color=orders)', fontweight='bold')
ax.grid(alpha=0.3)
cbar = plt.colorbar(sc, ax=ax); cbar.set_label('Orders')

# Days Span vs Open Rate
ax = axes[1]
sc = ax.scatter(df['days_span'], df['email_open_rate'], 
                c=df['count_placed_order'], cmap='viridis', alpha=0.5, s=15)
ax.set_xlabel('Days Span (Speed to Peak)')
ax.set_ylabel('Email Open Rate')
ax.set_title('Days Span vs Open Rate (color=orders)', fontweight='bold')
ax.grid(alpha=0.3)
cbar = plt.colorbar(sc, ax=ax); cbar.set_label('Orders')

plt.tight_layout()
plt.savefig('/work/frequency_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved")

# ============== 5. At-Risk / Winback Segment ==============
seg_labels = ['Retained\nCold Start', 'At-Risk\nCold Start', 'Retained\nGrowth', 'At-Risk\nGrowth',
              'Retained\nMature', 'At-Risk\nMature', 'Retained\nPeak']
seg_orders = [2.95, 4.42, 1.44, 0.19, 1.60, 1.95, 0.39]
seg_revenue = [277.0, 416.4, 139.7, 21.7, 177.5, 221.1, 48.1]
seg_colors = ['#2ecc71','#e74c3c','#3498db','#e74c3c','#f39c12','#e74c3c','#9b59b6']

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(seg_labels))
width = 0.35
bars1 = ax.bar(x - width/2, seg_orders, width, label='Avg Orders', color=seg_colors, alpha=0.8)
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, seg_revenue, width, label='Avg Revenue ($)', color=seg_colors, alpha=0.4)
ax.set_xticks(x); ax.set_xticklabels(seg_labels, fontsize=9)
ax.set_ylabel('Avg Orders', fontweight='bold'); ax2.set_ylabel('Avg Revenue ($)', fontweight='bold')
ax.set_title('At-Risk (Win-back Target) vs Retained by Lifecycle Stage', fontweight='bold')
ax.grid(axis='y', alpha=0.3)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
for i,v in enumerate(seg_orders): ax.text(i-width/2, v+0.08, f'{v:.2f}', ha='center', fontsize=8, fontweight='bold')
for i,v in enumerate(seg_revenue): ax2.text(i+width/2, v+3, f'${v:.0f}', ha='center', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/at_risk_segments.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved")