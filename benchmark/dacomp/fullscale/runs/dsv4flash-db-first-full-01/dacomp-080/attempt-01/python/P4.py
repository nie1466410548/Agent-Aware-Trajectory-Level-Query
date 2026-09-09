import pandas as pd, numpy as np

prof = pd.read_csv('/work/user_profile.csv')

# Final composite score: min-max scaled dimensions
freq_min, freq_max = prof.n_survey_responses.min(), prof.n_survey_responses.max()
prof['freq_score'] = (prof.n_survey_responses - freq_min) / (freq_max - freq_min) * 40
prof['completion_score'] = prof.completion_rate * 30
prof['channel_score'] = prof.n_channels / 5.0 * 20
prof['progress_score'] = prof.avg_progress / 100.0 * 10
prof['value_score'] = (prof.freq_score + prof.completion_score +
                       prof.channel_score + prof.progress_score)

# Tier assignment: one_time = single participation; then score thresholds
# calibrated so power+high are a small high-value minority
def tier(score, n):
    if n == 1:
        return 'one_time'
    if score < 35: return 'low_value'
    if score < 50: return 'medium_value'
    if score < 60: return 'high_value'
    return 'power_user'

prof['tier'] = [tier(s, n) for s, n in zip(prof.value_score, prof.n_survey_responses)]

print("Score: min %.1f max %.1f mean %.1f" % (prof.value_score.min(), prof.value_score.max(), prof.value_score.mean()))
print("\nTier sizes:")
tc = prof.tier.value_counts()
print(tc)
print("\nTier proportions:")
print((tc/tc.sum()).round(3))

# Value contribution per tier
cont = prof.groupby('tier').agg(
    n_users=('email','count'),
    total_responses=('n_survey_responses','sum'),
    total_completed=('n_completed','sum'),
    total_channels=('n_channels','sum'),
    avg_score=('value_score','mean'),
    avg_freq=('n_survey_responses','mean'),
    avg_completion=('completion_rate','mean'),
    avg_channels=('n_channels','mean'),
    avg_progress=('avg_progress','mean')
).sort_values('avg_score')
cont['pct_users'] = (cont.n_users/cont.n_users.sum()*100).round(1)
cont['pct_responses'] = (cont.total_responses/cont.total_responses.sum()*100).round(1)
cont['pct_completed'] = (cont.total_completed/cont.total_completed.sum()*100).round(1)
print("\nTier contribution table:")
print(cont.round(2))

prof.to_csv('/work/user_scored.csv', index=False)
