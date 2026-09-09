import pandas as pd

crit = pd.read_csv('/work/priority_ranking.csv')
crit_sorted = crit.sort_values('priority_rank')
tail = crit_sorted.iloc[70:]  # ranks 71-79 (0-indexed 70 onwards)
cols_show = ['priority_rank', 'job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
             'job_health_score', 'avg_career_development_score', 'retention_difficulty_level',
             'talent_saturation', 'avg_weekly_hours', 'io_ratio', 'priority_score']
print(tail[cols_show].round(3).to_string(index=False))
