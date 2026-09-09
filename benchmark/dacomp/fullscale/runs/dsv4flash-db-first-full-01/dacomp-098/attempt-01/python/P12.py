import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/work/contact_funnel_full.csv')
df['first_response_at'] = pd.to_datetime(df['first_response_at'])
df['demo_booked_at'] = pd.to_datetime(df['demo_booked_at'])
df['trial_activated_at'] = pd.to_datetime(df['trial_activated_at'])
df['paid_at'] = pd.to_datetime(df['paid_at'])

plt.rcParams.update({'figure.dpi': 100, 'font.size': 10})

# ============ FIG 1: Funnel conversion rates ============
fig, ax = plt.subplots(figsize=(8, 5))
stages = ['Conv→Demo', 'Demo→Trial', 'Trial→Paid']
bot_rates = [85.2, 88.6, 60.9]
human_rates = [86.1, 88.2, 61.4]
x = np.arange(len(stages))
w = 0.35
b1 = ax.bar(x - w/2, bot_rates, w, label='Bot first response', color='#1f77b4')
b2 = ax.bar(x + w/2, human_rates, w, label='Human first response', color='#ff7f0e')
ax.set_ylabel('Conversion rate (%)')
ax.set_title('Sales Funnel Conversion Rates by First Response Type')
ax.set_xticks(x); ax.set_xticklabels(stages)
ax.set_ylim(0, 100)
for bars in [b1, b2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{bar.get_height():.1f}%', ha='center', fontsize=9)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig1_funnel_rates.png')
plt.close()

# ============ FIG 2: Stage durations ============
fig, ax = plt.subplots(figsize=(8, 5))
dur_names = ['FirstResp→Demo', 'Demo→Trial', 'Trial→Paid']
bot_dur = [129.0, 9.5, 18.0]
human_dur = [121.0, 12.1, 22.2]
x = np.arange(len(dur_names))
b1 = ax.bar(x - w/2, bot_dur, w, label='Bot first response', color='#1f77b4')
b2 = ax.bar(x + w/2, human_dur, w, label='Human first response', color='#ff7f0e')
ax.set_ylabel('Average days')
ax.set_title('Average Stage Durations by First Response Type')
ax.set_xticks(x); ax.set_xticklabels(dur_names)
for bars in [b1, b2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                f'{bar.get_height():.1f}', ha='center', fontsize=9)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig2_durations.png')
plt.close()

# ============ FIG 3: Industry × Type paid conversion ============
fig, ax = plt.subplots(figsize=(9, 5))
industries = ['E-commerce', 'Media & Ent.', 'Manufacturing', 'SaaS', 'Travel']
bot_paid = [57.5, 62.5, 62.0, 56.5, 63.8]
human_paid = [69.9, 51.2, 65.4, 62.3, 56.9]
x = np.arange(len(industries))
b1 = ax.bar(x - w/2, bot_paid, w, label='Bot first response', color='#1f77b4')
b2 = ax.bar(x + w/2, human_paid, w, label='Human first response', color='#ff7f0e')
ax.set_ylabel('Paid conversion rate among trials (%)')
ax.set_title('Trial→Paid Conversion by Industry and First Response Type')
ax.set_xticks(x); ax.set_xticklabels(industries)
ax.set_ylim(0, 100)
for bars in [b1, b2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                f'{bar.get_height():.1f}', ha='center', fontsize=8)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig3_industry_paid.png')
plt.close()

# ============ FIG 4: Region × Type (demo and paid) ============
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
regions = ['Asia Pacific', 'Europe', 'Latin America', 'Middle East & Africa', 'North America']
bot_demo = [85.9, 79.2, 87.7, 87.9, 85.8]
human_demo = [84.7, 84.9, 85.7, 88.3, 86.9]
bot_paid = [61.7, 64.0, 63.6, 62.6, 53.3]
human_paid = [64.0, 61.5, 61.0, 58.2, 62.6]

x = np.arange(len(regions))
axes[0].bar(x - w/2, bot_demo, w, label='Bot', color='#1f77b4')
axes[0].bar(x + w/2, human_demo, w, label='Human', color='#ff7f0e')
axes[0].set_xticks(x); axes[0].set_xticklabels(regions, rotation=20, ha='right', fontsize=8)
axes[0].set_ylabel('Demo conversion (%)')
axes[0].set_title('Conv→Demo by Region')
axes[0].set_ylim(0, 100)
axes[0].legend()

axes[1].bar(x - w/2, bot_paid, w, label='Bot', color='#1f77b4')
axes[1].bar(x + w/2, human_paid, w, label='Human', color='#ff7f0e')
axes[1].set_xticks(x); axes[1].set_xticklabels(regions, rotation=20, ha='right', fontsize=8)
axes[1].set_ylabel('Paid conversion among trials (%)')
axes[1].set_title('Trial→Paid by Region')
axes[1].set_ylim(0, 100)
axes[1].legend()
plt.tight_layout()
plt.savefig('/work/fig4_region.png')
plt.close()

# ============ FIG 5: Intent × Type ============
fig, ax = plt.subplots(figsize=(8, 4.5))
intents = ['pricing', 'billing', 'demo_request']
bot_i = [60.7, 54.2, 100.0]
human_i = [61.4, 66.7, 58.8]
x = np.arange(len(intents))
b1 = ax.bar(x - w/2, bot_i, w, label='Bot first response', color='#1f77b4')
b2 = ax.bar(x + w/2, human_i, w, label='Human first response', color='#ff7f0e')
ax.set_ylabel('Paid conversion among trials (%)')
ax.set_title('Trial→Paid Conversion by Intent Label and First Response Type')
ax.set_xticks(x); ax.set_xticklabels(intents)
ax.set_ylim(0, 110)
for bars in [b1, b2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                f'{bar.get_height():.1f}', ha='center', fontsize=9)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig5_intent.png')
plt.close()

print("Figures saved:")
import os
for f in ['fig1_funnel_rates.png','fig2_durations.png','fig3_industry_paid.png','fig4_region.png','fig5_intent.png']:
    print(f"  /work/{f} ({os.path.getsize('/work/'+f)} bytes)")