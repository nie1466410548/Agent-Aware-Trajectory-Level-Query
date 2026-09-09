import pandas as pd

crit = pd.read_csv('/work/priority_ranking.csv')
crit_sorted = crit.sort_values('priority_rank')

# Print full list in a compact format
cols_show = ['priority_rank', 'job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
             'job_health_score', 'avg_career_development_score', 'retention_difficulty_level',
             'talent_saturation', 'avg_weekly_hours', 'io_ratio', 'priority_score']

pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 250)
print(crit_sorted[cols_show].to_string(index=False))

# Save a clean version for report reference
crit_sorted[cols_show].round(3).to_csv('/work/critical_list_clean.csv', index=False)
print("\nTotal critical:", len(crit_sorted))
