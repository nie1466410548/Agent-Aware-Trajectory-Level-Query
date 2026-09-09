import pandas as pd, numpy as np

prof = pd.read_csv('/work/user_profile.csv')

# ---- Composite Value Score (0-100) ----
# D1 Participation frequency (0-40): min-max scaled on observed range [1,13]
freq_min, freq_max = prof.n_survey_responses.min(), prof.n_survey_responses.max()
prof['freq_score'] = (prof.n_survey_responses - freq_min) / (freq_max - freq_min) * 40

# D2 Completion rate (0-30)
prof['completion_score'] = prof.completion_rate * 30

# D3 Cross-channel activity (0-20): n_channels out of 5 channels
prof['channel_score'] = prof.n_channels / 5.0 * 20

# D4 Engagement depth (0-10): avg progress
prof['progress_score'] = prof.avg_progress / 100.0 * 10

prof['value_score'] = (prof.freq_score + prof.completion_score +
                       prof.channel_score + prof.progress_score)

print("Score distribution:")
print(prof.value_score.describe())
print("\nPercentiles:", np.percentile(prof.value_score, [10,25,50,75,90,95,99]).round(1))

# Segment tiers aligned with cohort_analysis naming
def tier(score, n):
    if n == 1:
        return 'one_time'
    if score < 35: return 'low_value'
    if score < 55: return 'medium_value'
    if score < 75: return 'high_value'
    return 'power_user'

prof['tier'] = [tier(s, n) for s, n in zip(prof.value_score, prof.n_survey_responses)]
print("\nTier distribution:")
print(prof.tier.value_counts())
print(prof.tier.value_counts(normalize=True).round(3))
prof.to_csv('/work/user_scored.csv', index=False)
