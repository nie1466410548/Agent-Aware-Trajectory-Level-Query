import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

prof = pd.read_csv('/work/user_scored.csv')

# ---- Channel-level analysis: which channels appear in high-value users ----
# Recompute channel usage per user from response table (SQL) then join in Python
chan = db.frame(db.query("""
SELECT recipient_email AS email,
       MAX(CASE WHEN distribution_channel='email' THEN 1 ELSE 0 END) AS ch_email,
       MAX(CASE WHEN distribution_channel='sms' THEN 1 ELSE 0 END) AS ch_sms,
       MAX(CASE WHEN distribution_channel='mobile' THEN 1 ELSE 0 END) AS ch_mobile,
       MAX(CASE WHEN distribution_channel='web' THEN 1 ELSE 0 END) AS ch_web,
       MAX(CASE WHEN distribution_channel='social' THEN 1 ELSE 0 END) AS ch_social,
       COUNT(DISTINCT distribution_channel) AS n_channels
FROM qualtrics__response
GROUP BY recipient_email
"""))
prof = prof.merge(chan, on='email', how='left')

# Which channels are more prevalent among high+power users?
hp = prof[prof.tier.isin(['high_value','power_user'])]
rest = prof[~prof.tier.isin(['high_value','power_user'])]
channels = ['ch_email','ch_sms','ch_mobile','ch_web','ch_social']
print("Channel prevalence: High+Power vs rest")
comp = pd.DataFrame({
    'channel': ['email','sms','mobile','web','social'],
    'high_power_pct': [hp[c].mean()*100 for c in channels],
    'rest_pct': [rest[c].mean()*100 for c in channels]
})
comp['lift'] = comp.high_power_pct / comp.rest_pct
print(comp.round(1).to_string(index=False))

# ---- Channel usage by tier ----
ch_by_tier = prof.groupby('tier')[channels].mean()*100
print("\nChannel prevalence by tier (%):")
print(ch_by_tier.round(1).to_string())

# ---- Cohort table trends ----
cohort = db.frame(db.query("SELECT cohort_month, cohort_size, avg_responses_per_user, avg_completion_rate, power_users, high_value_users, medium_value_users, low_value_users, one_time_users, cohort_health_score FROM qualtrics__user_cohort_analysis ORDER BY cohort_month"))
cohort['cohort_month'] = pd.to_datetime(cohort['cohort_month'])
print("\nCohort table (last 4):")
print(cohort.tail(4).to_string())

# Tier proportions over time in cohort table
for col in ['power_users','high_value_users','medium_value_users','low_value_users','one_time_users']:
    cohort[col+'_pct'] = cohort[col] / cohort['cohort_size'] * 100
print("\nCohort tier proportions (mean %):")
print(cohort[['power_users_pct','high_value_users_pct','medium_value_users_pct','low_value_users_pct','one_time_users_pct']].mean().round(1))

# Save cohort trend chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(cohort.cohort_month, cohort.cohort_health_score, marker='o', color='#2ecc71')
ax1.set_title('Cohort Health Score Over Time', fontsize=13)
ax1.set_xlabel('Cohort Month')
ax1.set_ylabel('Health Score')
ax1.tick_params(axis='x', rotation=30)

tier_cols = ['power_users_pct','high_value_users_pct','medium_value_users_pct','low_value_users_pct','one_time_users_pct']
tier_labels = ['Power','High','Medium','Low','One-time']
for col, lab, color in zip(tier_cols, tier_labels, ['#2ecc71','#3498db','#f39c12','#e74c3c','#95a5a6']):
    ax2.plot(cohort.cohort_month, cohort[col], marker='.', label=lab, color=color)
ax2.set_title('Cohort Tier Composition Over Time', fontsize=13)
ax2.set_xlabel('Cohort Month')
ax2.set_ylabel('% of Cohort')
ax2.legend()
ax2.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig('/work/fig7_cohort_trends.png', dpi=120)
plt.close()
print("Saved fig7_cohort_trends.png")

# ---- Gap chart by region (transition recipe) ----
fig, ax = plt.subplots(figsize=(12, 5))
# Normalize gaps for plotting
gap_plot = prof.groupby('continent').apply(lambda g: pd.Series({
    'freq_gap': g[g.tier=='high_value'].n_survey_responses.mean() - g[g.tier=='medium_value'].n_survey_responses.mean(),
    'comp_gap': g[g.tier=='high_value'].completion_rate.mean() - g[g.tier=='medium_value'].completion_rate.mean(),
    'chan_gap': g[g.tier=='high_value'].n_channels.mean() - g[g.tier=='medium_value'].n_channels.mean(),
})).dropna()

x = np.arange(len(gap_plot))
w = 0.27
ax.bar(x-w, gap_plot['freq_gap'], w, label='Response Frequency Gap', color='#3498db')
ax.bar(x, gap_plot['comp_gap'], w, label='Completion Rate Gap', color='#2ecc71')
ax.bar(x+w, gap_plot['chan_gap'], w, label='Channel Count Gap', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels(gap_plot.index, rotation=15)
ax.set_ylabel('Medium → High Gap (High mean - Medium mean)')
ax.set_title('Transition Recipe by Continent: Medium→High Behavioral Gaps', fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig8_transition_by_region.png', dpi=120)
plt.close()
print("Saved fig8_transition_by_region.png")

prof.to_csv('/work/user_scored.csv', index=False)