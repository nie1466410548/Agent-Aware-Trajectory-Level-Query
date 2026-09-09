import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ========== MEMBERSHIP LEVEL COMPARISON ==========
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Membership Level Distribution
levels = ['Diamond Member', 'Regular Member', 'Gold Member', 'Silver Member', 'Platinum Member']
hv_mem = [10, 8, 6, 5, 4]
all_mem = [75, 97, 84, 99, 92]
# HV percentages (of 33 with membership)
hv_pct = [round(10/33*100, 1), round(8/33*100, 1), round(6/33*100, 1), round(5/33*100, 1), round(4/33*100, 1)]
all_pct = [round(75/447*100, 1), round(97/447*100, 1), round(84/447*100, 1), round(99/447*100, 1), round(92/447*100, 1)]

x = np.arange(len(levels))
w = 0.35
ax1 = axes[0, 0]
bars1 = ax1.bar(x - w/2, hv_pct, w, label='HV Customers (n=33)', color='#2E86AB', alpha=0.9)
bars2 = ax1.bar(x + w/2, all_pct, w, label='All Customers (n=447)', color='#A23B72', alpha=0.7)
ax1.set_ylabel('Percentage (%)', fontsize=11)
ax1.set_title('Membership Level Distribution', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(levels, fontsize=8, rotation=30)
ax1.legend(fontsize=9)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

# 2. Member Status
statuses = ['Normal', 'De-registered', 'Frozen']
hv_status = [12, 13, 8]
all_status = [147, 152, 148]
hv_sp = [round(12/33*100, 1), round(13/33*100, 1), round(8/33*100, 1)]
all_sp = [round(147/447*100, 1), round(152/447*100, 1), round(148/447*100, 1)]

ax2 = axes[0, 1]
x2 = np.arange(len(statuses))
bars1 = ax2.bar(x2 - w/2, hv_sp, w, label='HV Customers', color='#2E86AB', alpha=0.9)
bars2 = ax2.bar(x2 + w/2, all_sp, w, label='All Customers', color='#A23B72', alpha=0.7)
ax2.set_ylabel('Percentage (%)', fontsize=11)
ax2.set_title('Member Status', fontsize=13, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(statuses, fontsize=10)
ax2.legend(fontsize=9)
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)

# 3. Upgrade Requirements Met
upgrades = ['Yes', 'No']
hv_up = [19, 14]
all_up = [219, 228]
hv_up_pct = [19/33*100, 14/33*100]
all_up_pct = [219/447*100, 228/447*100]

ax3 = axes[0, 2]
x3 = np.arange(len(upgrades))
bars1 = ax3.bar(x3 - w/2, hv_up_pct, w, label='HV Customers', color='#2E86AB', alpha=0.9)
bars2 = ax3.bar(x3 + w/2, all_up_pct, w, label='All Customers', color='#A23B72', alpha=0.7)
ax3.set_ylabel('Percentage (%)', fontsize=11)
ax3.set_title('Upgrade Requirements Met', fontsize=13, fontweight='bold')
ax3.set_xticks(x3)
ax3.set_xticklabels(upgrades, fontsize=10)
ax3.legend(fontsize=9)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)

# 4. Tag Distribution (HV customers)
tags = ['High-Value\nCustomer', 'Newly\nRegistered', 'Key\nAccount', 'Gold\nCustomer', 'Temporary\nCustomer', 'Potential\nCustomer', 'Long-term\ncooperation', 'VIP', 'Under\nObservation']
hv_tag_cnt = [8, 7, 7, 6, 5, 5, 5, 4, 4]
all_tag_cnt = [70, 67, 58, 58, 69, 52, 78, 53, 61]

ax4 = axes[1, 0]
x4 = np.arange(len(tags))
bars1 = ax4.bar(x4 - w/2, hv_tag_cnt, w, label='HV Customers (n=51)', color='#2E86AB', alpha=0.9)
bars2 = ax4.bar(x4 + w/2, [c/619*100 for c in all_tag_cnt], w, label='All Tags %', color='#A23B72', alpha=0.7)
ax4.set_ylabel('Count / Percentage', fontsize=11)
ax4.set_title('Customer Tags Distribution', fontsize=13, fontweight='bold')
ax4.set_xticks(x4)
ax4.set_xticklabels(tags, fontsize=7, rotation=20)
ax4.legend(fontsize=9)
for bar in bars1:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2, str(int(bar.get_height())), ha='center', va='bottom', fontsize=8)

# 5. Credit Grade Distribution (via transaction accounts)
grades = ['A', 'AAA', 'BBB', 'AA', 'BB']
hv_cr = [11, 7, 6, 5, 3]
all_cr = [63, 52, 49, 47, 48]
hv_cr_pct = [round(11/32*100, 1), round(7/32*100, 1), round(6/32*100, 1), round(5/32*100, 1), round(3/32*100, 1)]
all_cr_pct = [round(63/259*100, 1), round(52/259*100, 1), round(49/259*100, 1), round(47/259*100, 1), round(48/259*100, 1)]

ax5 = axes[1, 1]
x5 = np.arange(len(grades))
bars1 = ax5.bar(x5 - w/2, hv_cr_pct, w, label='HV Customers (n=32)', color='#2E86AB', alpha=0.9)
bars2 = ax5.bar(x5 + w/2, all_cr_pct, w, label='All Tx Customers (n=259)', color='#A23B72', alpha=0.7)
ax5.set_ylabel('Percentage (%)', fontsize=11)
ax5.set_title('Credit Grade Distribution', fontsize=13, fontweight='bold')
ax5.set_xticks(x5)
ax5.set_xticklabels(grades, fontsize=10)
ax5.legend(fontsize=9)
for bar in bars1:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

# 6. Contract Type
ctypes = ['Sales Contract', 'Service contract', 'Purchase Contract']
hv_ct = [18, 12, 7]
all_ct = [165, 192, 170]
hv_ct_pct = [round(18/37*100, 1), round(12/37*100, 1), round(7/37*100, 1)]
all_ct_pct = [round(165/527*100, 1), round(192/527*100, 1), round(170/527*100, 1)]

ax6 = axes[1, 2]
x6 = np.arange(len(ctypes))
bars1 = ax6.bar(x6 - w/2, hv_ct_pct, w, label='HV Customers (n=37)', color='#2E86AB', alpha=0.9)
bars2 = ax6.bar(x6 + w/2, all_ct_pct, w, label='All Customers (n=527)', color='#A23B72', alpha=0.7)
ax6.set_ylabel('Percentage (%)', fontsize=11)
ax6.set_title('Contract Type Distribution', fontsize=13, fontweight='bold')
ax6.set_xticks(x6)
ax6.set_xticklabels(ctypes, fontsize=9, rotation=15)
ax6.legend(fontsize=9)
for bar in bars1:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('/work/hv_customer_profile_1.png', dpi=150, bbox_inches='tight')
plt.close()

# ========== SECOND PAGE: ADDITIONAL INSIGHTS ==========
fig2, axes2 = plt.subplots(2, 3, figsize=(18, 12))

# 1. Payment Methods
pmethods = ['WeChat Pay', 'UnionPay', 'Cash', 'Alipay']
hv_pm = [19, 19, 20, 13]
all_pm = [119, 123, 120, 121]
hv_pm_pct = [round(19/71*100, 1), round(19/71*100, 1), round(20/71*100, 1), round(13/71*100, 1)]
all_pm_pct = [round(119/483*100, 1), round(123/483*100, 1), round(120/483*100, 1), round(121/483*100, 1)]

ax1 = axes2[0, 0]
x1 = np.arange(len(pmethods))
w2 = 0.35
bars1 = ax1.bar(x1 - w2/2, hv_pm_pct, w2, label='HV Customers (n=71)', color='#2E86AB', alpha=0.9)
bars2 = ax1.bar(x1 + w2/2, all_pm_pct, w2, label='All Customers (n=483)', color='#A23B72', alpha=0.7)
ax1.set_ylabel('Percentage (%)', fontsize=11)
ax1.set_title('Payment Method Preference', fontsize=13, fontweight='bold')
ax1.set_xticks(x1)
ax1.set_xticklabels(pmethods, fontsize=9)
ax1.legend(fontsize=9)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

# 2. Channel Source
channels = ['Douyin\nShort Video', 'Offline\nStore', 'WeChat\nAds', 'Baidu\nPromotion', 'Ground\nPromotion']
hv_ch = [11, 9, 4, 4, 3]
all_ch = [104, 94, 97, 81, 95]
hv_ch_pct = [round(11/31*100, 1), round(9/31*100, 1), round(4/31*100, 1), round(4/31*100, 1), round(3/31*100, 1)]
all_ch_pct = [round(104/471*100, 1), round(94/471*100, 1), round(97/471*100, 1), round(81/471*100, 1), round(95/471*100, 1)]

ax2 = axes2[0, 1]
x2 = np.arange(len(channels))
bars1 = ax2.bar(x2 - w2/2, hv_ch_pct, w2, label='HV Customers (n=31)', color='#2E86AB', alpha=0.9)
bars2 = ax2.bar(x2 + w2/2, all_ch_pct, w2, label='All Customers (n=471)', color='#A23B72', alpha=0.7)
ax2.set_ylabel('Percentage (%)', fontsize=11)
ax2.set_title('Acquisition Channel Source', fontsize=13, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(channels, fontsize=8)
ax2.legend(fontsize=9)
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

# 3. Gender Distribution
genders = ['Female', 'Male']
hv_g = [23, 16]
all_g = [273, 254]
hv_g_pct = [round(23/39*100, 1), round(16/39*100, 1)]
all_g_pct = [round(273/527*100, 1), round(254/527*100, 1)]

ax3 = axes2[0, 2]
x3 = np.arange(len(genders))
bars1 = ax3.bar(x3 - w2/2, hv_g_pct, w2, label='HV Customers (n=39)', color='#2E86AB', alpha=0.9)
bars2 = ax3.bar(x3 + w2/2, all_g_pct, w2, label='All Customers (n=527)', color='#A23B72', alpha=0.7)
ax3.set_ylabel('Percentage (%)', fontsize=11)
ax3.set_title('Gender Distribution', fontsize=13, fontweight='bold')
ax3.set_xticks(x3)
ax3.set_xticklabels(genders, fontsize=10)
ax3.legend(fontsize=9)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)

# 4. Service Ticket Satisfaction
scores = ['1', '2', '3', '4', '5']
hv_tk = [7, 1, 5, 4, 3]
all_tk = [88, 86, 83, 79, 92]
hv_tk_pct = [round(7/20*100, 1), round(1/20*100, 1), round(5/20*100, 1), round(4/20*100, 1), round(3/20*100, 1)]
all_tk_pct = [round(88/428*100, 1), round(86/428*100, 1), round(83/428*100, 1), round(79/428*100, 1), round(92/428*100, 1)]

ax4 = axes2[1, 0]
x4 = np.arange(len(scores))
bars1 = ax4.bar(x4 - w2/2, hv_tk_pct, w2, label='HV Customers (n=20)', color='#2E86AB', alpha=0.9)
bars2 = ax4.bar(x4 + w2/2, all_tk_pct, w2, label='All Customers (n=428)', color='#A23B72', alpha=0.7)
ax4.set_ylabel('Percentage (%)', fontsize=11)
ax4.set_title('Service Ticket Satisfaction', fontsize=13, fontweight='bold')
ax4.set_xlabel('Satisfaction Score (1=Low, 5=High)', fontsize=10)
ax4.set_xticks(x4)
ax4.set_xticklabels(scores, fontsize=10)
ax4.legend(fontsize=9)
for bar in bars1:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
ax4.text(2, 18, f'Avg HV: 2.75\nAvg All: 3.00', ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))

# 5. Product/Service Orders
products = ['Firewall\nSecurity', 'Database\nBackup', 'Enterprise\nEmail', 'Cloud\nStorage', 'Video\nConference']
hv_prod = [11, 9, 3, 3, 2]
all_prod = [90, 81, 84, 89, 91]
hv_prod_pct = [round(11/28*100, 1), round(9/28*100, 1), round(3/28*100, 1), round(3/28*100, 1), round(2/28*100, 1)]
all_prod_pct = [round(90/435*100, 1), round(81/435*100, 1), round(84/435*100, 1), round(89/435*100, 1), round(91/435*100, 1)]

ax5 = axes2[1, 1]
x5 = np.arange(len(products))
bars1 = ax5.bar(x5 - w2/2, hv_prod_pct, w2, label='HV Customers (n=28)', color='#2E86AB', alpha=0.9)
bars2 = ax5.bar(x5 + w2/2, all_prod_pct, w2, label='All Customers (n=435)', color='#A23B72', alpha=0.7)
ax5.set_ylabel('Percentage (%)', fontsize=11)
ax5.set_title('Subscribed Products/Services', fontsize=13, fontweight='bold')
ax5.set_xticks(x5)
ax5.set_xticklabels(products, fontsize=8)
ax5.legend(fontsize=9)
for bar in bars1:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

# 6. Membership Points Comparison
metrics = ['Current Points', 'Lifetime Points']
hv_pts = [2837, 12288]
all_pts = [2438, 12726]

ax6 = axes2[1, 2]
x6 = np.arange(len(metrics))
bars1 = ax6.bar(x6 - w2/2, hv_pts, w2, label='HV Customers (n=33)', color='#2E86AB', alpha=0.9)
bars2 = ax6.bar(x6 + w2/2, all_pts, w2, label='All Customers (n=447)', color='#A23B72', alpha=0.7)
ax6.set_ylabel('Average Points', fontsize=11)
ax6.set_title('Membership Points Average', fontsize=13, fontweight='bold')
ax6.set_xticks(x6)
ax6.set_xticklabels(metrics, fontsize=10)
ax6.legend(fontsize=9)
for bar in bars1:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50, f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50, f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('/work/hv_customer_profile_2.png', dpi=150, bbox_inches='tight')
plt.close()

print("Visualizations saved successfully")