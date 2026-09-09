import pandas as pd, numpy as np

prof = pd.read_csv('/work/user_profile.csv')

# Redesign scoring with broader differentiation
# D1: Participation frequency (0-40) - log-based scaling
max_freq = prof.n_survey_responses.max()
prof['freq_score'] = np.log1p(prof.n_survey_responses) / np.log1p(max_freq) * 40

# D2: Completion rate (0-30)
prof['completion_score'] = prof.completion_rate * 30

# D3: Cross-channel activity (0-20)
prof['channel_score'] = prof.n_channels / 5.0 * 20

# D4: Engagement depth (0-10)
prof['progress_score'] = prof.avg_progress / 100.0 * 10

prof['value_score'] = (prof.freq_score + prof.completion_score +
                       prof.channel_score + prof.progress_score)

print("Score distribution:")
print(prof.value_score.describe())
print("Percentiles:", np.percentile(prof.value_score, [10,25,50,75,90,95,99]).round(1))

# Define tier thresholds aligned with cohort table proportions
# Target: one_time ~17%, low ~25%, medium ~35%, high ~15%, power ~8%
# We'll use n_survey_responses==1 for one_time, then quartile-like thresholds
# Based on score distribution: p33~33, p67~47, p85~57, p95~65
# Let's set thresholds to get reasonable tier sizes
low_th = 35
med_th = 50
high_th = 65
power_th = 75

def tier2(score, n):
    if n == 1:
        return 'one_time'
    if score < low_th: return 'low_value'
    if score < med_th: return 'medium_value'
    if score < high_th: return 'high_value'
    if score < power_th: return 'power_user'
    return 'power_user'

prof['tier'] = [tier2(s, n) for s, n in zip(prof.value_score, prof.n_survey_responses)]
print("\nTier distribution:")
print(prof.tier.value_counts())
print(prof.tier.value_counts(normalize=True).round(3))

# Try different thresholds to get closer to cohort proportions
# Let's try percentile-based thresholds
pcts = np.percentile(prof.value_score[prof.n_survey_responses > 1], 
                     [0, 25, 50, 75, 90])
print(f"\nScore percentiles (excluding one-time): {pcts}")

# Try a more aggressive power_user threshold
# Let's try: score >= 60 = high_value, >= 70 = power_user
def tier3(score, n):
    if n == 1:
        return 'one_time'
    if score < 35: return 'low_value'
    if score < 50: return 'medium_value'
    if score < 62: return 'high_value'
    return 'power_user'

prof['tier'] = [tier3(s, n) for s, n in zip(prof.value_score, prof.n_survey_responses)]
print("\nTier distribution (adjusted):")
print(prof.tier.value_counts())
print(prof.tier.value_counts(normalize=True).round(3))
prof.to_csv('/work/user_scored.csv', index=False)