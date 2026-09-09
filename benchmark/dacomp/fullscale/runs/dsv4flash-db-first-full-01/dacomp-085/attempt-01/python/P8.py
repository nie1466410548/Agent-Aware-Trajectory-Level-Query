import pandas as pd, numpy as np, json

rows = []
with open('/results/S15.rows.jsonl') as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

cols = ['job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
        'job_health_score', 'avg_career_development_score', 'retention_difficulty_level',
        'is_work_shift_required', 'avg_weekly_hours', 'current_employees_count',
        'active_positions_count', 'talent_saturation', 'talent_quality_index']

df = pd.DataFrame(rows, columns=cols)
df['health_norm'] = df['job_health_score'] / 100.0
df['dev_norm'] = df['avg_career_development_score'] / 5.0
df['output_index'] = 0.5 * df['health_norm'] + 0.5 * df['dev_norm']
sat_max, sat_min = df['talent_saturation'].max(), df['talent_saturation'].min()
hrs_max, hrs_min = df['avg_weekly_hours'].max(), df['avg_weekly_hours'].min()
df['sat_norm'] = (df['talent_saturation'] - sat_min) / (sat_max - sat_min)
df['hrs_norm'] = (df['avg_weekly_hours'] - hrs_min) / (hrs_max - hrs_min)
df['input_index'] = 0.5 * df['sat_norm'] + 0.5 * df['hrs_norm']
df['io_ratio'] = df['input_index'] / (df['output_index'] + 0.01)
df['is_mismatch'] = df['output_index'] <= df['output_index'].quantile(0.25)
df['is_imbalanced'] = df['io_ratio'] >= df['io_ratio'].quantile(0.75)

mis = df[df['is_mismatch']]

# Summary stats for mismatch profiles
print("=== MISMATCH PROFILE SUMMARY (167 profiles) ===")
print(f"Tier 1: {mis['job_value_tier'].value_counts().get('Tier 1', 0)}")
print(f"Tier 2: {mis['job_value_tier'].value_counts().get('Tier 2', 0)}")
print(f"High competition: {mis['talent_competition_level'].value_counts().get('High', 0)}")
print(f"Very High competition: {mis['talent_competition_level'].value_counts().get('Very High', 0)}")
print(f"\nRetention difficulty:")
print(mis['retention_difficulty_level'].value_counts().to_string())
print(f"\nShift required: {mis['is_work_shift_required'].sum()} out of {len(mis)}")
print(f"\nAvg health: {mis['job_health_score'].mean():.2f}")
print(f"Avg dev: {mis['avg_career_development_score'].mean():.2f}")
print(f"Avg saturation: {mis['talent_saturation'].mean():.3f}")
print(f"Avg quality: {mis['talent_quality_index'].mean():.5f}")
print(f"Avg hours: {mis['avg_weekly_hours'].mean():.1f}")

# Top job titles among mismatch
print("\n=== Top 10 Job Titles in Mismatch Group ===")
print(mis['job_title'].value_counts().head(10).to_string())

# For the 79 critical profiles: summary
crit = df[df['is_mismatch'] & df['is_imbalanced']]
print("\n\n=== CRITICAL PROFILES SUMMARY (79 profiles) ===")
print(f"Avg health: {crit['job_health_score'].mean():.2f}")
print(f"Avg dev: {crit['avg_career_development_score'].mean():.2f}")
print(f"Avg saturation: {crit['talent_saturation'].mean():.3f}")
print(f"Avg hours: {crit['avg_weekly_hours'].mean():.1f}")
print(f"Avg io_ratio: {crit['io_ratio'].mean():.3f}")

# For the 88 mismatch-only (not imbalanced) profiles
mis_only = df[df['is_mismatch'] & ~df['is_imbalanced']]
print("\n\n=== MISMATCH-ONLY PROFILES (88 profiles) ===")
print(f"Avg health: {mis_only['job_health_score'].mean():.2f}")
print(f"Avg dev: {mis_only['avg_career_development_score'].mean():.2f}")
print(f"Avg saturation: {mis_only['talent_saturation'].mean():.3f}")
print(f"Avg hours: {mis_only['avg_weekly_hours'].mean():.1f}")

# For the 86 imbalanced-only (not mismatch) profiles
imb_only = df[~df['is_mismatch'] & df['is_imbalanced']]
print("\n\n=== IMBALANCED-ONLY PROFILES (86 profiles) ===")
print(f"Avg health: {imb_only['job_health_score'].mean():.2f}")
print(f"Avg dev: {imb_only['avg_career_development_score'].mean():.2f}")
print(f"Avg saturation: {imb_only['talent_saturation'].mean():.3f}")
print(f"Avg hours: {imb_only['avg_weekly_hours'].mean():.1f}")