import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

prof = pd.read_csv('/work/user_scored.csv')

# Re-acquire channel data
chan = db.frame(db.query("""
SELECT recipient_email AS email,
       MAX(CASE WHEN distribution_channel='email' THEN 1 ELSE 0 END) AS ch_email,
       MAX(CASE WHEN distribution_channel='sms' THEN 1 ELSE 0 END) AS ch_sms,
       MAX(CASE WHEN distribution_channel='mobile' THEN 1 ELSE 0 END) AS ch_mobile,
       MAX(CASE WHEN distribution_channel='web' THEN 1 ELSE 0 END) AS ch_web,
       MAX(CASE WHEN distribution_channel='social' THEN 1 ELSE 0 END) AS ch_social
FROM qualtrics__response
GROUP BY recipient_email
"""))

# Drop old n_channels from prof before merge
if 'n_channels_x' in prof.columns:
    prof = prof.drop(columns=['n_channels_x'])
if 'n_channels_y' in prof.columns:
    prof = prof.drop(columns=['n_channels_y'])

prof = prof.merge(chan, on='email', how='left')

# Use original n_channels from the profile
# Actually the original n_channels was already in prof. Let me check
print("Columns:", [c for c in prof.columns if 'channel' in c.lower()])

# Let's just use the original n_channels
# Recompute channel prevalence
hp = prof[prof.tier.isin(['high_value','power_user'])]
rest = prof[~prof.tier.isin(['high_value','power_user'])]
channels = ['ch_email','ch_sms','ch_mobile','ch_web','ch_social']
print("\nChannel prevalence: High+Power vs rest")
comp = pd.DataFrame({
    'channel': ['email','sms','mobile','web','social'],
    'high_power_pct': [hp[c].mean()*100 for c in channels],
    'rest_pct': [rest[c].mean()*100 for c in channels]
})
comp['lift'] = comp.high_power_pct / comp.rest_pct
print(comp.round(1).to_string(index=False))

# ---- Gap chart by region ----
# Recompute region gaps without groupby apply
gap_rows = []
for cont in prof.continent.unique():
    sub = prof[prof.continent == cont]
    m = sub[sub.tier == 'medium_value']
    h = sub[sub.tier == 'high_value']
    if len(m) > 15 and len(h) > 15:
        gap_rows.append({
            'continent': cont,
            'freq_gap': h.n_survey_responses.mean() - m.n_survey_responses.mean(),
            'comp_gap': h.completion_rate.mean() - m.completion_rate.mean(),
            'chan_gap': h.n_channels.mean() - m.n_channels.mean()
        })

gap_plot = pd.DataFrame(gap_rows).set_index('continent')
print("\nTransition gaps by continent:")
print(gap_plot.round(3))

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(gap_plot))
w = 0.27
ax.bar(x-w, gap_plot['freq_gap'], w, label='Response Frequency Gap', color='#3498db')
ax.bar(x, gap_plot['comp_gap'], w, label='Completion Rate Gap', color='#2ecc71')
ax.bar(x+w, gap_plot['chan_gap'], w, label='Channel Count Gap', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels(gap_plot.index, rotation=15)
ax.set_ylabel('Medium → High Gap (mean difference)')
ax.set_title('Medium→High Behavioral Gaps by Continent', fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig8_transition_by_region.png', dpi=120)
plt.close()
print("Saved fig8_transition_by_region.png")